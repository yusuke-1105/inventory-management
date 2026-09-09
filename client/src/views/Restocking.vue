<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.budgetLabel') }}</h3>
        </div>
        <div class="budget-slider">
          <input
            type="range"
            min="0"
            :max="maxBudget"
            :step="budgetStep"
            v-model.number="budget"
            class="budget-range"
          />
          <div class="budget-readout">{{ currencySymbol }}{{ budget.toLocaleString() }}</div>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card info">
          <div class="stat-label">{{ t('restocking.recommendedCount') }}</div>
          <div class="stat-value">{{ recommendedItems.length }}</div>
        </div>
        <div class="stat-card success">
          <div class="stat-label">{{ t('restocking.totalCost') }}</div>
          <div class="stat-value">{{ currencySymbol }}{{ totalCost.toLocaleString() }}</div>
        </div>
        <div class="stat-card warning">
          <div class="stat-label">{{ t('restocking.remainingBudget') }}</div>
          <div class="stat-value">{{ currencySymbol }}{{ remainingBudget.toLocaleString() }}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendedItems') }}</h3>
        </div>
        <div v-if="recommendedItems.length === 0" class="empty-state">
          {{ t('restocking.noRecommendations') }}
        </div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.itemName') }}</th>
                <th>{{ t('restocking.table.trend') }}</th>
                <th>{{ t('restocking.table.quantity') }}</th>
                <th>{{ t('restocking.table.unitCost') }}</th>
                <th>{{ t('restocking.table.lineCost') }}</th>
                <th>{{ t('restocking.table.leadTime') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recommendedItems" :key="item.item_sku">
                <td><strong>{{ item.item_sku }}</strong></td>
                <td>{{ item.item_name }}</td>
                <td>
                  <span :class="['badge', item.trend]">
                    {{ t(`trends.${item.trend}`) }}
                  </span>
                </td>
                <td>{{ item.quantity }}</td>
                <td>{{ currencySymbol }}{{ item.unit_cost.toLocaleString() }}</td>
                <td><strong>{{ currencySymbol }}{{ item.lineCost.toLocaleString() }}</strong></td>
                <td>{{ item.lead_time_days }} {{ t('common.days') }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <button
          class="place-order-btn"
          :disabled="recommendedItems.length === 0 || placing"
          @click="placeOrder"
        >
          {{ placing ? t('restocking.placingOrder') : t('restocking.placeOrder') }}
        </button>

        <div v-if="placeError" class="error">{{ placeError }}</div>

        <div v-if="lastOrder" class="order-confirmation">
          {{ t('restocking.orderPlaced', { orderNumber: lastOrder.order_number }) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency } = useI18n()

    const currencySymbol = computed(() => {
      return currentCurrency.value === 'JPY' ? '¥' : '$'
    })

    const loading = ref(true)
    const error = ref(null)
    const forecasts = ref([])

    const budget = ref(0)
    const maxBudget = ref(10000)
    const budgetStep = 50

    const placing = ref(false)
    const placeError = ref(null)
    const lastOrder = ref(null)

    // Candidate items: forecasted growth gap becomes the restock quantity.
    // Items with no forecasted growth (or a shrinking forecast) have nothing to restock.
    const candidateItems = computed(() => {
      return forecasts.value
        .map(forecast => {
          const quantity = Math.max(0, forecast.forecasted_demand - forecast.current_demand)
          return {
            ...forecast,
            quantity,
            lineCost: quantity * forecast.unit_cost
          }
        })
        .filter(item => item.quantity > 0)
    })

    // Urgency-ranked greedy budget allocation:
    // 1. Sort candidates by trend urgency (increasing > stable > decreasing), then by
    //    line cost ascending so cheaper items within the same urgency tier are considered first.
    // 2. Walk the sorted list and add each item IN FULL if it fits in the remaining budget.
    //    Items that don't fit are skipped (not partially filled) so a later, cheaper item
    //    further down the list still has a chance to fit.
    const recommendedItems = computed(() => {
      const urgencyRank = { increasing: 0, stable: 1, decreasing: 2 }

      const sorted = [...candidateItems.value].sort((a, b) => {
        const rankDiff = urgencyRank[a.trend] - urgencyRank[b.trend]
        if (rankDiff !== 0) return rankDiff
        return a.lineCost - b.lineCost
      })

      const recommended = []
      let remaining = budget.value

      for (const item of sorted) {
        if (item.lineCost <= remaining) {
          recommended.push(item)
          remaining -= item.lineCost
        }
      }

      return recommended
    })

    const totalCost = computed(() => {
      return recommendedItems.value.reduce((sum, item) => sum + item.lineCost, 0)
    })

    const remainingBudget = computed(() => {
      return budget.value - totalCost.value
    })

    const loadForecasts = async () => {
      try {
        loading.value = true
        error.value = null
        forecasts.value = await api.getDemandForecasts()

        // Seed the slider with a non-trivial starting value so the page isn't empty
        // on first paint. ~25% of total candidate line cost is an arbitrary demo
        // default, not a business rule.
        const totalCandidateCost = candidateItems.value.reduce((sum, item) => sum + item.lineCost, 0)
        budget.value = Math.round(totalCandidateCost * 0.25)
        maxBudget.value = Math.max(1000, Math.round(totalCandidateCost))
      } catch (err) {
        error.value = 'Failed to load demand forecasts: ' + err.message
      } finally {
        loading.value = false
      }
    }

    const placeOrder = async () => {
      if (recommendedItems.value.length === 0) return

      placing.value = true
      placeError.value = null

      try {
        lastOrder.value = await api.createRestockingOrder({
          budget: budget.value,
          items: recommendedItems.value.map(i => ({
            sku: i.item_sku,
            name: i.item_name,
            quantity: i.quantity,
            unit_cost: i.unit_cost,
            lead_time_days: i.lead_time_days
          }))
        })
      } catch (err) {
        placeError.value = 'Failed to place restocking order: ' + err.message
      } finally {
        placing.value = false
      }
    }

    onMounted(loadForecasts)

    return {
      t,
      currencySymbol,
      loading,
      error,
      budget,
      maxBudget,
      budgetStep,
      candidateItems,
      recommendedItems,
      totalCost,
      remainingBudget,
      placing,
      placeError,
      lastOrder,
      placeOrder
    }
  }
}
</script>

<style scoped>
.budget-slider {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.budget-range {
  flex: 1;
  accent-color: #2563eb;
  height: 6px;
  cursor: pointer;
}

.budget-readout {
  min-width: 120px;
  text-align: right;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
}

.empty-state {
  text-align: center;
  padding: var(--space-6);
  color: #64748b;
  font-size: 0.938rem;
}

.place-order-btn {
  margin-top: 1.25rem;
  padding: 0.625rem 1.5rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.place-order-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.place-order-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.order-confirmation {
  margin-top: var(--space-4);
  background: #d1fae5;
  border: 1px solid #a7f3d0;
  color: #065f46;
  padding: var(--space-4);
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 500;
}
</style>
