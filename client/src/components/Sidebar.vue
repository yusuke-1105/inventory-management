<template>
  <aside class="sidebar">
    <div class="brand">
      <h1>{{ t('nav.companyName') }}</h1>
      <span class="brand-subtitle">{{ t('nav.subtitle') }}</span>
    </div>

    <nav class="nav-list">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <rect x="2.5" y="2.5" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
          <rect x="9.5" y="2.5" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
          <rect x="2.5" y="9.5" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
          <rect x="9.5" y="9.5" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span>{{ t('nav.overview') }}</span>
      </router-link>

      <router-link to="/inventory" class="nav-item" :class="{ active: $route.path === '/inventory' }">
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M2.5 5.5L9 2.5L15.5 5.5L9 8.5L2.5 5.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <path d="M2.5 5.5V12.5L9 15.5L15.5 12.5V5.5" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <path d="M9 8.5V15.5" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span>{{ t('nav.inventory') }}</span>
      </router-link>

      <router-link to="/orders" class="nav-item" :class="{ active: $route.path === '/orders' }">
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M5 2.5H13C13.5523 2.5 14 2.94772 14 3.5V15.5L9 13.5L4 15.5V3.5C4 2.94772 4.44772 2.5 5 2.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <path d="M6.5 6.5H11.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M6.5 9.5H11.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>{{ t('nav.orders') }}</span>
      </router-link>

      <router-link to="/spending" class="nav-item" :class="{ active: $route.path === '/spending' }">
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <circle cx="9" cy="9" r="6.5" stroke="currentColor" stroke-width="1.5"/>
          <path d="M9 5.5V12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M11 7.25C11 6.28 10.1 5.5 9 5.5C7.9 5.5 7 6.28 7 7.25C7 8.22 7.9 9 9 9C10.1 9 11 9.78 11 10.75C11 11.72 10.1 12.5 9 12.5C7.9 12.5 7 11.72 7 10.75" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>{{ t('nav.finance') }}</span>
      </router-link>

      <router-link to="/demand" class="nav-item" :class="{ active: $route.path === '/demand' }">
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M2.5 13.5L7 9L10 12L15.5 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M11.5 6H15.5V10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>{{ t('nav.demandForecast') }}</span>
      </router-link>

      <router-link to="/restocking" class="nav-item" :class="{ active: $route.path === '/restocking' }">
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M15 9C15 5.68629 12.3137 3 9 3C6.75 3 4.79 4.24 3.75 6.08" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M3.75 3V6.08H6.83" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M3 9C3 12.3137 5.68629 15 9 15C11.25 15 13.21 13.76 14.25 11.92" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M14.25 15V11.92H11.17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>{{ t('nav.restocking') }}</span>
      </router-link>

      <router-link to="/reports" class="nav-item" :class="{ active: $route.path === '/reports' }">
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M5 2.5H11L14.5 6V14.5C14.5 15.0523 14.0523 15.5 13.5 15.5H4.5C3.94772 15.5 3.5 15.0523 3.5 14.5V3.5C3.5 2.94772 3.94772 2.5 4.5 2.5H5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <path d="M11 2.5V6H14.5" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <path d="M6.5 9.5V12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M9 8V12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M11.5 10.5V12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>{{ t('nav.reports') }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <LanguageSwitcher />
      <ProfileMenu
        @show-profile-details="$emit('show-profile-details')"
        @show-tasks="$emit('show-tasks')"
      />
    </div>
  </aside>
</template>

<script setup>
import { useI18n } from '../composables/useI18n'
import ProfileMenu from './ProfileMenu.vue'
import LanguageSwitcher from './LanguageSwitcher.vue'

defineEmits(['show-profile-details', 'show-tasks'])

const { t } = useI18n()
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.brand {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-5) var(--space-5) var(--space-4);
  border-bottom: 1px solid #e2e8f0;
}

.brand h1 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.brand-subtitle {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 400;
}

.nav-list {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px var(--space-3);
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: var(--radius-sm);
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
}

.nav-icon {
  flex-shrink: 0;
  color: inherit;
}

.nav-item:hover {
  color: #0f172a;
  background: #f1f5f9;
}

.nav-item.active {
  color: #2563eb;
  background: #eff6ff;
  border-left-color: #2563eb;
  font-weight: 600;
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-3);
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
}

.sidebar-footer :deep(.language-switcher),
.sidebar-footer :deep(.profile-menu) {
  width: 100%;
}

.sidebar-footer :deep(.language-button),
.sidebar-footer :deep(.profile-button) {
  width: 100%;
}
</style>
