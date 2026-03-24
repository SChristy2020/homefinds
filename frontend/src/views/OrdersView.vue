<template>
  <div>
    <!-- Lookup form -->
    <div v-if="!userStore.currentUser" class="orders-lookup">
      <div class="lookup-title">{{ i18n.t('orders.lookupTitle') }}</div>
      <div class="form-group">
        <label>{{ i18n.t('orders.namePlaceholder') }}</label>
        <input v-model="form.name" :placeholder="i18n.t('orders.namePlaceholder')" :class="{ 'input-error': errors.name }" @input="onNameInput" />
        <p v-if="errors.name" class="field-error">{{ errors.name }}</p>
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="your@email.com" :class="{ 'input-error': errors.email }" @input="errors.email = ''" />
        <p v-if="errors.email" class="field-error">{{ errors.email }}</p>
      </div>
      <div class="form-group" style="margin-bottom:16px;">
        <label>Phone</label>
        <input v-model="form.phone" placeholder="(xxx)xxx-xxxx" :class="{ 'input-error': errors.phone }" @input="errors.phone = ''" />
        <p v-if="errors.phone" class="field-error">{{ errors.phone }}</p>
      </div>
      <button class="btn-primary" :disabled="userStore.loading" @click="handleLookup">
        {{ userStore.loading ? '...' : i18n.t('orders.sent') }}
      </button>
      <p v-if="userStore.error" class="error-msg">{{ i18n.t('orders.error') }}</p>
    </div>

    <!-- Logged in -->
    <div v-else>
      <!-- Orders table -->
      <div class="orders-table-wrap">
        <p class="orders-greeting">
          {{ i18n.t('orders.greeting', { name: userStore.currentUser.first_name }) }}
        </p>
        <h2 class="orders-section-title">{{ i18n.t('orders.sectionTitle') }}</h2>

        <!-- DataTable toolbar -->
        <div class="dt-toolbar">
          <div class="dt-info">
            {{ i18n.t('orders.dtShowing', { from: dtFrom, to: dtTo, total: filteredOrders.length }) }}
          </div>
          <div v-if="isAdmin" class="dt-status-filters">
            <button :class="['dt-filter-btn', statusFilter.length === 0 ? 'active' : '']" @click="statusFilter = []">{{ i18n.t('orders.filterAll') }}</button>
            <button :class="['dt-filter-btn', statusFilter.includes('pending_payment') ? 'active' : '']" @click="toggleStatusFilter('pending_payment')">{{ i18n.t('orders.pending_payment') }}</button>
            <button :class="['dt-filter-btn', statusFilter.includes('paid') ? 'active' : '']" @click="toggleStatusFilter('paid')">{{ i18n.t('orders.paid') }}</button>
            <button :class="['dt-filter-btn', statusFilter.includes('picked_up') ? 'active' : '']" @click="toggleStatusFilter('picked_up')">{{ i18n.t('orders.picked_up') }}</button>
            <button :class="['dt-filter-btn', statusFilter.includes('cancelled') ? 'active' : '']" @click="toggleStatusFilter('cancelled')">{{ i18n.t('orders.cancelled') }}</button>
          </div>
          <input v-model="searchQuery" class="dt-search" :placeholder="i18n.t('orders.dtSearch')" />
        </div>

        <div class="table-scroll-wrap">
        <table class="orders-table">
          <thead>
            <tr>
              <th class="sortable" @click="toggleSort('id')">
                {{ i18n.t('orders.orderNo') }}<SortIcon col="id" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('items')">
                {{ i18n.t('orders.itemCount') }}<SortIcon col="items" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('total')">
                {{ i18n.t('orders.orderTotal') }}<SortIcon col="total" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('paid')">
                {{ i18n.t('orders.payStatus') }}<SortIcon col="paid" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th v-if="isAdmin">{{ i18n.t('orders.adminNotes') }}</th>
              <th class="sortable" @click="toggleSort('pickup')">
                {{ i18n.t('orders.pickupTimeLabel') }}<SortIcon col="pickup" :active="sortColumn" :dir="sortDirection" />
              </th>
              <template v-if="isAdmin">
                <th class="sortable" @click="toggleSort('buyer')">
                  {{ i18n.t('orders.buyer') }}<SortIcon col="buyer" :active="sortColumn" :dir="sortDirection" />
                </th>
                <th>{{ i18n.t('orders.buyerEmail') }}</th>
                <th>{{ i18n.t('orders.buyerPhone') }}</th>
                <th>{{ i18n.t('orders.buyerZelleRefund') }}</th>
              </template>
              <th class="sortable" @click="toggleSort('created')">
                {{ i18n.t('orders.createdAt') }}<SortIcon col="created" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th v-if="isAdmin" class="sortable" @click="toggleSort('updated')">
                {{ i18n.t('orders.updatedAt') }}<SortIcon col="updated" :active="sortColumn" :dir="sortDirection" />
              </th>
            </tr>
          </thead>
          <tbody v-if="filteredOrders.length === 0">
            <tr>
              <td :colspan="isAdmin ? 11 : 6" class="td-empty">{{ i18n.t('orders.noOrdersTable') }}</td>
            </tr>
          </tbody>
          <tbody v-for="order in paginatedOrders" :key="order.id">
            <!-- Order summary row -->
            <tr class="order-row" :class="{ expanded: expandedOrderId === order.id, 'order-row-dimmed': isAllSoldCancelled(order) }" @click="toggleExpand(order.id)">
              <td class="td-order-no">{{ order.order_number }}</td>
              <td>{{ activeItemCount(order) }}</td>
              <td>{{ orderTotal(order) }}</td>
              <td :class="editingStatusOrderId !== order.id ? statusClass(order) : ''">
                <template v-if="isAdmin">
                  <template v-if="editingStatusOrderId !== order.id">
                    <span class="status-display">
                      <span>{{ statusLabel(order) }}</span>
                      <button class="btn-edit-icon" @click.stop="startEditStatus(order)" title="編輯">
                        <Pencil :size="12" />
                      </button>
                    </span>
                  </template>
                  <template v-else>
                    <div class="status-edit-wrap" @click.stop>
                      <select v-model="editingStatusValue" class="status-select">
                        <option value="pending_payment">{{ i18n.t('orders.pending_payment') }}</option>
                        <option value="paid">{{ i18n.t('orders.paid') }}</option>
                        <option value="picked_up">{{ i18n.t('orders.picked_up') }}</option>
                        <option value="cancelled">{{ i18n.t('orders.cancelled') }}</option>
                      </select>
                      <div class="pickup-edit-actions">
                        <button class="btn-save-pickup" @click.stop="saveStatus(order)">{{ i18n.t('orders.savePickup') }}</button>
                        <button class="btn-cancel-pickup" @click.stop="cancelEditStatus">{{ i18n.t('orders.cancelPickupEdit') }}</button>
                      </div>
                    </div>
                  </template>
                </template>
                <template v-else>
                  {{ statusLabel(order) }}
                </template>
              </td>
              <td v-if="isAdmin" class="td-admin-notes" @click.stop>
                <template v-if="editingNotesOrderId !== order.id">
                  <span class="notes-display">
                    <span class="notes-text">{{ order.admin_notes || '—' }}</span>
                    <button class="btn-edit-icon" @click.stop="startEditNotes(order)" title="編輯">
                      <Pencil :size="12" />
                    </button>
                  </span>
                </template>
                <template v-else>
                  <div class="notes-edit-wrap">
                    <textarea v-model="editingNotesValue" class="notes-textarea" rows="2" @click.stop />
                    <div class="pickup-edit-actions">
                      <button class="btn-save-pickup" @click.stop="saveAdminNotes(order)">{{ i18n.t('orders.savePickup') }}</button>
                      <button class="btn-cancel-pickup" @click.stop="cancelEditNotes">{{ i18n.t('orders.cancelPickupEdit') }}</button>
                    </div>
                  </div>
                </template>
              </td>
              <td class="td-pickup">
                <template v-if="order.order_status === 'cancelled'">
                  <span class="no-pickup-text">{{ i18n.t('orders.noPickup') }}</span>
                </template>
                <template v-else-if="editingOrderId !== order.id">
                  <span>{{ formatDateTime(order.pickup_time) }}</span>
                  <button class="btn-edit-icon" @click.stop="startEditPickup(order)" title="編輯">
                    <Pencil :size="12" />
                  </button>
                </template>
                <template v-else>
                  <div class="pickup-edit-wrap" @click.stop>
                    <PickupDatePicker v-model="editPickupValue" />
                    <div class="pickup-edit-actions">
                      <button class="btn-save-pickup" @click.stop="savePickupTime(order)">{{ i18n.t('orders.savePickup') }}</button>
                      <button class="btn-cancel-pickup" @click.stop="cancelEditPickup">{{ i18n.t('orders.cancelPickupEdit') }}</button>
                    </div>
                  </div>
                </template>
              </td>
              <template v-if="isAdmin">
                <td class="td-buyer">{{ order.buyer_last_name }} {{ order.buyer_first_name }}</td>
                <td class="td-buyer-info">{{ order.buyer_email }}</td>
                <td class="td-buyer-info">{{ order.buyer_phone }}</td>
                <td class="td-buyer-info">{{ order.buyer_zelle_refund === 'other' ? order.buyer_zelle_refund_other : order.buyer_zelle_refund === 'email' ? 'Email' : '電話' }}</td>
              </template>
              <td class="td-created">{{ formatDateTime(order.created_at) }}</td>
              <td v-if="isAdmin" class="td-created">{{ formatDateTime(order.updated_at) }}</td>
            </tr>

            <!-- Expanded items row -->
            <tr v-if="expandedOrderId === order.id" class="expand-row">
              <td :colspan="isAdmin ? 12 : 6">
                <OrderItemList :items="order.items.filter(i => i.status !== 'cancelled')" :orderStatus="order.order_status" @cancel="handleCancel" />

                <!-- Total summary -->
                <div class="order-summary">
                  <span class="summary-label">
                    {{ i18n.t('cart.itemCountPrefix') }} {{ activeItemCount(order) }} {{ i18n.t('cart.itemCountSuffix') }}
                  </span>
                  <span class="summary-price">
                    <span v-if="hasDiscount(order)" class="strikethrough">${{ orderOriginalTotal(order) }}</span>
                    ${{ orderTotal(order) }}
                    <span v-if="isAllSoldCancelled(order)" class="all-sold-note">{{ i18n.t('orders.allSoldNote') }}</span>
                  </span>
                </div>

                <!-- Not-first warning -->
                <p v-if="hasNotFirstPosition(order)" class="not-first-warning">
                  {{ i18n.t('orderSuccess.notFirstWarning') }}
                </p>
              </td>
            </tr>
          </tbody>
        </table>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="dt-pagination">
          <button class="dt-page-btn" :disabled="currentPage === 1" @click="currentPage = 1">«</button>
          <button class="dt-page-btn" :disabled="currentPage === 1" @click="currentPage--">‹</button>
          <button
            v-for="p in pageNumbers"
            :key="p"
            class="dt-page-btn"
            :class="{ active: p === currentPage }"
            @click="currentPage = p"
          >{{ p }}</button>
          <button class="dt-page-btn" :disabled="currentPage === totalPages" @click="currentPage++">›</button>
          <button class="dt-page-btn" :disabled="currentPage === totalPages" @click="currentPage = totalPages">»</button>
        </div>
      </div>

      <!-- 租屋訂單 -->
      <div class="reservations-section">
        <h2 class="orders-section-title reservations-section-title">{{ i18n.t('reservations.sectionTitle') }}</h2>

        <!-- Reservations toolbar -->
        <div class="dt-toolbar">
          <div class="dt-info">
            {{ i18n.t('orders.dtShowing', { from: resDtFrom, to: resDtTo, total: filteredReservations.length }) }}
          </div>
          <div v-if="isAdmin" class="dt-status-filters">
            <button :class="['dt-filter-btn', resStatusFilter.length === 0 ? 'active' : '']" @click="resStatusFilter = []">{{ i18n.t('orders.filterAll') }}</button>
            <button v-for="s in ORDER_STATUSES" :key="s" :class="['dt-filter-btn', resStatusFilter.includes(s) ? 'active' : '']" @click="toggleResStatusFilter(s)">{{ resStatusLabel(s) }}</button>
          </div>
          <input v-model="resSearchQuery" class="dt-search" :placeholder="i18n.t('reservations.dtSearch')" />
        </div>

        <div class="table-scroll-wrap">
        <table class="orders-table reservations-table">
          <thead>
            <tr>
              <th class="sortable" @click="toggleResSort('id')">{{ i18n.t('reservations.resNo') }}<SortIcon col="id" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th class="sortable" @click="toggleResSort('check_in')">{{ i18n.t('reservations.checkIn') }}<SortIcon col="check_in" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th class="sortable" @click="toggleResSort('check_out')">{{ i18n.t('reservations.checkOut') }}<SortIcon col="check_out" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th class="sortable" @click="toggleResSort('nights')">{{ i18n.t('reservations.nights') }}<SortIcon col="nights" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th class="sortable" @click="toggleResSort('deposit')">{{ i18n.t('reservations.depositAmount') }}<SortIcon col="deposit" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th class="sortable" @click="toggleResSort('total')">{{ i18n.t('reservations.totalPrice') }}<SortIcon col="total" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th class="sortable" @click="toggleResSort('status')">{{ i18n.t('reservations.orderStatus') }}<SortIcon col="status" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th v-if="isAdmin">{{ i18n.t('reservations.detailAdminNote') }}</th>
              <template v-if="isAdmin">
                <th class="sortable" @click="toggleResSort('buyer')">{{ i18n.t('reservations.buyer') }}<SortIcon col="buyer" :active="resSortColumn" :dir="resSortDirection" /></th>
                <th>{{ i18n.t('reservations.buyerEmail') }}</th>
                <th>{{ i18n.t('reservations.buyerPhone') }}</th>
                <th>{{ i18n.t('reservations.buyerZelleRefund') }}</th>
              </template>
              <th class="sortable" @click="toggleResSort('created')">{{ i18n.t('reservations.createdAt') }}<SortIcon col="created" :active="resSortColumn" :dir="resSortDirection" /></th>
              <th v-if="isAdmin" class="sortable" @click="toggleResSort('updated')">{{ i18n.t('reservations.updatedAt') }}<SortIcon col="updated" :active="resSortColumn" :dir="resSortDirection" /></th>
            </tr>
          </thead>
          <tbody v-if="filteredReservations.length === 0">
            <tr>
              <td :colspan="isAdmin ? 13 : 8" class="td-empty">{{ i18n.t('reservations.noReservations') }}</td>
            </tr>
          </tbody>
          <tbody v-for="res in resPaginatedReservations" v-else :key="res.id">
            <tr class="order-row" :class="{ expanded: expandedResId === res.id }" @click="toggleExpandRes(res.id)">
              <td class="td-order-no">{{ res.order_number || res.id }}</td>
              <td>{{ formatDate(res.check_in) }}</td>
              <td>{{ formatDate(res.check_out) }}</td>
              <td>{{ res.nights }}</td>
              <td>${{ res.deposit_amount }}</td>
              <td>${{ res.total_price }}</td>
              <td :class="editingStatusResId !== res.id ? orderStatusClass(res.order_status) : ''">
                <template v-if="!isAdmin || editingStatusResId !== res.id">
                  <span class="status-display">
                    <span>{{ resStatusLabel(res.order_status) }}</span>
                    <button v-if="isAdmin" class="btn-edit-icon" @click.stop="startEditResStatus(res)" title="編輯">
                      <Pencil :size="12" />
                    </button>
                  </span>
                </template>
                <template v-else>
                  <div class="status-edit-wrap" @click.stop>
                    <select v-model="editingStatusValue" class="status-select">
                      <option v-for="s in ORDER_STATUSES" :key="s" :value="s">{{ resStatusLabel(s) }}</option>
                    </select>
                    <div class="pickup-edit-actions">
                      <button class="btn-save-pickup" @click.stop="saveResStatus(res)">{{ i18n.t('orders.savePickup') }}</button>
                      <button class="btn-cancel-pickup" @click.stop="cancelEditStatus">{{ i18n.t('orders.cancelPickupEdit') }}</button>
                    </div>
                  </div>
                </template>
              </td>
              <td v-if="isAdmin" class="td-admin-notes" @click.stop>
                <template v-if="editingAdminNoteResId !== res.id">
                  <span class="notes-display">
                    <span class="notes-text">{{ res.admin_note || '—' }}</span>
                    <button class="btn-edit-icon" @click.stop="startEditAdminNote(res)" title="編輯備註"><Pencil :size="12" /></button>
                  </span>
                </template>
                <template v-else>
                  <div class="notes-edit-wrap" @click.stop>
                    <textarea v-model="editingAdminNoteValue" class="notes-textarea" rows="2" @click.stop />
                    <div class="pickup-edit-actions">
                      <button class="btn-save-pickup" @click.stop="saveAdminNote(res)">{{ i18n.t('orders.savePickup') }}</button>
                      <button class="btn-cancel-pickup" @click.stop="cancelEditAdminNote">{{ i18n.t('orders.cancelPickupEdit') }}</button>
                    </div>
                  </div>
                </template>
              </td>
              <template v-if="isAdmin">
                <td class="td-buyer">{{ res.buyer_last_name }} {{ res.buyer_first_name }}</td>
                <td class="td-buyer-info">{{ res.buyer_email }}</td>
                <td class="td-buyer-info">{{ res.buyer_phone }}</td>
                <td class="td-buyer-info">{{ res.buyer_zelle_refund === 'other' ? res.buyer_zelle_refund_other : res.buyer_zelle_refund === 'email' ? 'Email' : '電話' }}</td>
              </template>
              <td class="td-created">{{ formatDateTime(res.created_at) }}</td>
              <td v-if="isAdmin" class="td-created">{{ formatDateTime(res.updated_at) }}</td>
            </tr>

            <!-- Expanded reservation details row -->
            <tr v-if="expandedResId === res.id" class="expand-row">
              <td :colspan="isAdmin ? 14 : 8">
                <div class="res-expand-grid">
                  <div class="res-detail-cell">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailFirstName') }}</span>
                    <span class="res-detail-value">{{ isAdmin ? res.buyer_first_name : userStore.currentUser?.first_name }}</span>
                  </div>
                  <div class="res-detail-cell">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailLastName') }}</span>
                    <span class="res-detail-value">{{ isAdmin ? res.buyer_last_name : userStore.currentUser?.last_name }}</span>
                  </div>
                  <div class="res-detail-cell">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailSalutation') }}</span>
                    <span class="res-detail-value">{{ isAdmin ? res.buyer_salutation : userStore.currentUser?.salutation }}</span>
                  </div>
                  <div class="res-detail-cell">
                    <span class="res-detail-label">Email</span>
                    <span class="res-detail-value">{{ isAdmin ? res.buyer_email : userStore.currentUser?.email }}</span>
                  </div>
                  <div class="res-detail-cell">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailPhone') }}</span>
                    <span class="res-detail-value">{{ isAdmin ? res.buyer_phone : userStore.currentUser?.phone }}</span>
                  </div>
                  <div class="res-detail-cell">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailBirthYear') }}</span>
                    <span class="res-detail-value">{{ res.birth_year || '—' }}</span>
                  </div>
                  <div class="res-detail-cell">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailOccupation') }}</span>
                    <span class="res-detail-value">{{ res.occupation || '—' }}</span>
                  </div>
                  <div class="res-detail-cell">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailGuestsPets') }}</span>
                    <span class="res-detail-value">{{ res.has_guests_or_pets ? i18n.t('reservations.detailGuestsPetsYes') : i18n.t('reservations.detailGuestsPetsNo') }}</span>
                  </div>
                  <div class="res-detail-cell res-detail-cell--span3">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailGuestsPetsDesc') }}</span>
                    <span class="res-detail-value">{{ res.guests_pets_description || '—' }}</span>
                  </div>
                  <div class="res-detail-cell res-detail-cell--span3">
                    <span class="res-detail-label">{{ i18n.t('reservations.detailSpecialRequests') }}</span>
                    <span class="res-detail-value">{{ res.special_requests || '—' }}</span>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        </div>

        <!-- Reservations Pagination -->
        <div v-if="resTotalPages > 1" class="dt-pagination">
          <button class="dt-page-btn" :disabled="resCurrentPage === 1" @click="resCurrentPage = 1">«</button>
          <button class="dt-page-btn" :disabled="resCurrentPage === 1" @click="resCurrentPage--">‹</button>
          <button
            v-for="p in resPageNumbers"
            :key="p"
            class="dt-page-btn"
            :class="{ active: p === resCurrentPage }"
            @click="resCurrentPage = p"
          >{{ p }}</button>
          <button class="dt-page-btn" :disabled="resCurrentPage === resTotalPages" @click="resCurrentPage++">›</button>
          <button class="dt-page-btn" :disabled="resCurrentPage === resTotalPages" @click="resCurrentPage = resTotalPages">»</button>
        </div>
      </div>

      <!-- 取貨與租屋行事曆 (admin only) -->
      <div v-if="isAdmin" class="pickup-calendar-section">
        <h2 class="orders-section-title">取貨與租屋行事曆</h2>
        <div class="cal-nav">
          <button class="cal-nav-btn" @click="calPrevMonth">‹</button>
          <span class="cal-month-label">{{ calMonthLabel }}</span>
          <button class="cal-nav-btn" @click="calNextMonth">›</button>
        </div>
        <div class="cal-grid">
          <div class="cal-day-header" v-for="d in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="d">{{ d }}</div>
          <div
            v-for="cell in calCells"
            :key="cell.key"
            class="cal-day"
            :class="{ 'cal-day--other': !cell.inMonth, 'cal-day--today': cell.isToday }"
          >
            <div class="cal-day-num" :class="{ 'cal-day-num--today': cell.isToday }">{{ cell.day }}</div>
            <div
              v-for="event in cell.events"
              :key="event.id"
              class="cal-event"
              :class="[
                event.type === 'reservation' ? 'cal-event--reservation' : '',
                event.spanPos ? `cal-event--span-${event.spanPos}` : '',
                event.type === 'reservation' && calHoverResId === event.data.id ? 'cal-event--res-hovered' : ''
              ]"
              :title="event.fullLabel"
              @mouseenter="event.type === 'reservation' && (calHoverResId = event.data.id)"
              @mouseleave="calHoverResId = null"
              @click.stop="calSelectedItem = event"
            >{{ event.label }}</div>
          </div>
        </div>
      </div>

      <!-- Calendar item detail modal -->
      <Teleport to="body">
        <div v-if="calSelectedItem" class="cal-modal-backdrop" @click.self="calSelectedItem = null">
          <div class="cal-modal">
            <div class="cal-modal-header">
              <span class="cal-modal-title">{{ calSelectedItem.data.order_number || calSelectedItem.data.id }}</span>
              <button class="cal-modal-close" @click="calSelectedItem = null">✕</button>
            </div>
            <div class="cal-modal-body">

              <!-- 購物訂單 -->
              <template v-if="calSelectedItem.type === 'order'">
                <div class="cal-modal-grid">
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.payStatus') }}</span>
                    <span :class="statusClass(calSelectedItem.data)">{{ statusLabel(calSelectedItem.data) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.pickupTimeLabel') }}</span>
                    <span>{{ formatDateTime(calSelectedItem.data.pickup_time) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.buyer') }}</span>
                    <span>{{ calSelectedItem.data.buyer_last_name }} {{ calSelectedItem.data.buyer_first_name }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.buyerEmail') }}</span>
                    <span>{{ calSelectedItem.data.buyer_email || '—' }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.buyerPhone') }}</span>
                    <span>{{ calSelectedItem.data.buyer_phone || '—' }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.orderTotal') }}</span>
                    <span>${{ orderTotal(calSelectedItem.data) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.createdAt') }}</span>
                    <span>{{ formatDateTime(calSelectedItem.data.created_at) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('orders.updatedAt') }}</span>
                    <span>{{ formatDateTime(calSelectedItem.data.updated_at) }}</span>
                  </div>
                  <div class="cal-modal-field cal-modal-field--full">
                    <span class="cal-modal-label">{{ i18n.t('orders.adminNotes') }}</span>
                    <span class="cal-modal-notes">{{ calSelectedItem.data.admin_notes || '—' }}</span>
                  </div>
                </div>
                <div class="cal-modal-items-title">{{ i18n.t('orders.itemCount') }}</div>
                <OrderItemList
                  :items="calSelectedItem.data.items.filter(i => i.status !== 'cancelled')"
                  :orderStatus="calSelectedItem.data.order_status"
                  @cancel="() => {}"
                />
              </template>

              <!-- 租屋訂單 -->
              <template v-else>
                <div class="cal-modal-grid">
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.orderStatus') }}</span>
                    <span :class="orderStatusClass(calSelectedItem.data.order_status)">{{ resStatusLabel(calSelectedItem.data.order_status) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.nights') }}</span>
                    <span>{{ calSelectedItem.data.nights }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.checkIn') }}</span>
                    <span>{{ formatDate(calSelectedItem.data.check_in) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.checkOut') }}</span>
                    <span>{{ formatDate(calSelectedItem.data.check_out) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.depositAmount') }}</span>
                    <span>${{ calSelectedItem.data.deposit_amount }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.totalPrice') }}</span>
                    <span>${{ calSelectedItem.data.total_price }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.buyer') }}</span>
                    <span>{{ calSelectedItem.data.buyer_last_name }} {{ calSelectedItem.data.buyer_first_name }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.buyerEmail') }}</span>
                    <span>{{ calSelectedItem.data.buyer_email || '—' }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.buyerPhone') }}</span>
                    <span>{{ calSelectedItem.data.buyer_phone || '—' }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.detailBirthYear') }}</span>
                    <span>{{ calSelectedItem.data.birth_year || '—' }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.detailOccupation') }}</span>
                    <span>{{ calSelectedItem.data.occupation || '—' }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.detailGuestsPets') }}</span>
                    <span>{{ calSelectedItem.data.has_guests_or_pets ? i18n.t('reservations.detailGuestsPetsYes') : i18n.t('reservations.detailGuestsPetsNo') }}</span>
                  </div>
                  <div class="cal-modal-field cal-modal-field--full">
                    <span class="cal-modal-label">{{ i18n.t('reservations.detailGuestsPetsDesc') }}</span>
                    <span class="cal-modal-notes">{{ calSelectedItem.data.guests_pets_description || '—' }}</span>
                  </div>
                  <div class="cal-modal-field cal-modal-field--full">
                    <span class="cal-modal-label">{{ i18n.t('reservations.detailSpecialRequests') }}</span>
                    <span class="cal-modal-notes">{{ calSelectedItem.data.special_requests || '—' }}</span>
                  </div>
                  <div class="cal-modal-field cal-modal-field--full">
                    <span class="cal-modal-label">{{ i18n.t('reservations.detailAdminNote') }}</span>
                    <span class="cal-modal-notes">{{ calSelectedItem.data.admin_note || '—' }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.createdAt') }}</span>
                    <span>{{ formatDateTime(calSelectedItem.data.created_at) }}</span>
                  </div>
                  <div class="cal-modal-field">
                    <span class="cal-modal-label">{{ i18n.t('reservations.updatedAt') }}</span>
                    <span>{{ formatDateTime(calSelectedItem.data.updated_at) }}</span>
                  </div>
                </div>
              </template>

            </div>
          </div>
        </div>
      </Teleport>

      <!-- 購物須知 -->
      <div class="shopping-guide-wrap">
        <button class="guide-toggle-btn" @click="shoppingGuideOpen = !shoppingGuideOpen">
          <span>{{ i18n.t('guide.sectionTitle') }}</span>
          <ChevronDown v-if="!shoppingGuideOpen" :size="16" />
          <ChevronUp v-else :size="16" />
        </button>
        <div v-if="shoppingGuideOpen" class="guide-collapse-body">
          <ShoppingGuideContent />
        </div>
      </div>

      <!-- 房間預訂流程說明 -->
      <div class="shopping-guide-wrap">
        <button class="guide-toggle-btn" @click="rentGuideOpen = !rentGuideOpen">
          <span>{{ i18n.t('guide.rentSectionTitle') }}</span>
          <ChevronDown v-if="!rentGuideOpen" :size="16" />
          <ChevronUp v-else :size="16" />
        </button>
        <div v-if="rentGuideOpen" class="guide-collapse-body">
          <div v-if="roomBookingDescription" class="rent-guide-content" v-html="roomBookingDescription"></div>
          <p v-else class="rent-guide-empty">{{ i18n.t('guide.rentGuideEmpty') }}</p>
        </div>
      </div>

      <div class="back-btn-wrap">
        <button class="btn-outline back-btn" @click="reset">
          <ArrowLeft :size="14" />{{ i18n.t('orders.back') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ArrowLeft, Pencil, ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-vue-next'
import { useOrdersStore } from '@/stores/orders'
import { useReservationsStore } from '@/stores/reservations'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useI18nStore } from '@/stores/i18n'
import OrderItemList from '@/components/orders/OrderItemList.vue'
import ShoppingGuideContent from '@/components/shared/ShoppingGuideContent.vue'
import PickupDatePicker from '@/components/shared/PickupDatePicker.vue'
import { api } from '@/utils/api'

const ordersStore = useOrdersStore()
const reservationsStore = useReservationsStore()
const userStore = useUserStore()
const toast = useToastStore()
const i18n = useI18nStore()

const isAdmin = computed(() => userStore.currentUser?.is_admin === 1)

const shoppingGuideOpen = ref(false)
const rentGuideOpen = ref(false)
const roomBookingMap = ref({})
const roomBookingDescription = computed(() =>
  roomBookingMap.value[i18n.locale] || roomBookingMap.value['zh-TW'] || ''
)

const form = ref({ name: '', email: '', phone: '' })
const errors = ref({ name: '', email: '', phone: '' })

const expandedOrderId = ref(null)
const expandedResId = ref(null)

// ── DataTable state ───────────────────────────────────────────────────────────
const searchQuery = ref('')
const statusFilter = ref([])
const currentPage = ref(1)
const pageSize = 10
const sortColumn = ref('id')
const sortDirection = ref('desc')

const filteredOrders = computed(() => {
  let orders = ordersStore.orders
  if (statusFilter.value.length > 0) {
    orders = orders.filter(o => statusFilter.value.includes(o.order_status))
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    orders = orders.filter(o =>
      (o.order_number || '').toLowerCase().includes(q) ||
      statusLabel(o).toLowerCase().includes(q)
    )
  }
  return [...orders].sort((a, b) => {
    let aVal, bVal
    if (sortColumn.value === 'id')     { aVal = a.id; bVal = b.id }
    else if (sortColumn.value === 'items')  { aVal = activeItemCount(a); bVal = activeItemCount(b) }
    else if (sortColumn.value === 'total')  { aVal = parseFloat(orderTotal(a)); bVal = parseFloat(orderTotal(b)) }
    else if (sortColumn.value === 'paid')   { const rank = { picked_up: 3, paid: 2, pending_payment: 1, cancelled: 0 }; aVal = rank[a.order_status] ?? 0; bVal = rank[b.order_status] ?? 0 }
    else if (sortColumn.value === 'pickup') {
      const nullVal = sortDirection.value === 'asc' ? Infinity : -Infinity
      aVal = (a.order_status !== 'cancelled' && a.pickup_time) ? new Date(a.pickup_time).getTime() : nullVal
      bVal = (b.order_status !== 'cancelled' && b.pickup_time) ? new Date(b.pickup_time).getTime() : nullVal
    }
    else if (sortColumn.value === 'created') { aVal = a.created_at || ''; bVal = b.created_at || '' }
    else if (sortColumn.value === 'updated') { aVal = a.updated_at || ''; bVal = b.updated_at || '' }
    else if (sortColumn.value === 'buyer') { aVal = (a.buyer_last_name || '') + (a.buyer_first_name || ''); bVal = (b.buyer_last_name || '') + (b.buyer_first_name || '') }
    else { aVal = a.id; bVal = b.id }
    if (aVal < bVal) return sortDirection.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortDirection.value === 'asc' ? 1 : -1
    return 0
  })
})

const totalPages = computed(() => Math.ceil(filteredOrders.value.length / pageSize))
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredOrders.value.slice(start, start + pageSize)
})
const dtFrom = computed(() => filteredOrders.value.length === 0 ? 0 : (currentPage.value - 1) * pageSize + 1)
const dtTo = computed(() => Math.min(currentPage.value * pageSize, filteredOrders.value.length))
const pageNumbers = computed(() => {
  const total = totalPages.value
  const cur = currentPage.value
  const delta = 2
  const range = []
  for (let i = Math.max(1, cur - delta); i <= Math.min(total, cur + delta); i++) range.push(i)
  return range
})

watch(searchQuery, () => { currentPage.value = 1 })
watch(statusFilter, () => { currentPage.value = 1 }, { deep: true })

function toggleStatusFilter(s) {
  const idx = statusFilter.value.indexOf(s)
  statusFilter.value = idx === -1
    ? [...statusFilter.value, s]
    : statusFilter.value.filter(x => x !== s)
}

function toggleSort(col) {
  if (sortColumn.value === col) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = col
    sortDirection.value = 'asc'
  }
  currentPage.value = 1
}

// Sort icon inline component
const SortIcon = {
  props: ['col', 'active', 'dir'],
  components: { ChevronUp, ChevronDown, ChevronsUpDown },
  template: `
    <span class="sort-icon">
      <ChevronUp v-if="active === col && dir === 'asc'" :size="12" />
      <ChevronDown v-else-if="active === col && dir === 'desc'" :size="12" />
      <ChevronsUpDown v-else :size="12" />
    </span>
  `
}

onMounted(async () => {
  try {
    const rooms = await api.get('/api/room')
    if (rooms.length) {
      const room = rooms[0]
      const map = {}
      for (const t of (room.translations || [])) {
        map[t.locale] = t.booking_description || ''
      }
      roomBookingMap.value = map
    }
  } catch {}

  if (userStore.currentUser) {
    if (userStore.currentUser.is_admin === 1) {
      await Promise.all([
        ordersStore.fetchAllOrders(),
        reservationsStore.fetchAllReservations(),
      ])
    } else if (ordersStore.orders.length === 0) {
      await Promise.all([
        ordersStore.fetchOrdersByUser(userStore.currentUser.id),
        reservationsStore.fetchReservationsByUser(userStore.currentUser.id),
      ])
    }
  }
})
const editingOrderId = ref(null)
const editPickupValue = ref('')
const editingStatusOrderId = ref(null)
const editingStatusValue = ref('')
const editingNotesOrderId = ref(null)
const editingNotesValue = ref('')

function onNameInput() {
  form.value.name = form.value.name.replace(/[^a-zA-Z\u4e00-\u9fff\u3400-\u4dbf\s'-]/g, '')
  errors.value.name = ''
}

function validate() {
  errors.value = { name: '', email: '', phone: '' }
  if (!form.value.name.trim()) {
    errors.value.name = i18n.t('orders.invalidName')
  }
  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRe.test(form.value.email)) {
    errors.value.email = i18n.t('orders.invalidEmail')
  }
  const phoneRe = /^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$/
  if (!phoneRe.test(form.value.phone.trim())) {
    errors.value.phone = i18n.t('orders.invalidPhone')
  }
  return !errors.value.name && !errors.value.email && !errors.value.phone
}

async function handleLookup() {
  if (!validate()) return
  window.gtag?.('event', 'order_lookup')
  const user = await userStore.lookup(form.value.name, form.value.email, form.value.phone)
  if (user) {
    if (user.is_admin === 1) {
      await Promise.all([
        ordersStore.fetchAllOrders(),
        reservationsStore.fetchAllReservations(),
      ])
    } else {
      await Promise.all([
        ordersStore.fetchOrdersByUser(user.id),
        reservationsStore.fetchReservationsByUser(user.id),
      ])
    }
  }
}

function toggleExpandRes(resId) {
  expandedResId.value = expandedResId.value === resId ? null : resId
}

function toggleExpand(orderId) {
  expandedOrderId.value = expandedOrderId.value === orderId ? null : orderId
  if (editingOrderId.value && editingOrderId.value !== orderId) {
    editingOrderId.value = null
  }
}

function startEditPickup(order) {
  editingOrderId.value = order.id
  editPickupValue.value = toPickerFormat(order.pickup_time)
}

function cancelEditPickup() {
  editingOrderId.value = null
  editPickupValue.value = ''
}

async function savePickupTime(order) {
  const isoStr = fromPickerFormat(editPickupValue.value)
  await ordersStore.updatePickupTime(order.id, isoStr)
  toast.show(i18n.t('orders.savePickupToast'))
  editingOrderId.value = null
}

function startEditStatus(order) {
  editingStatusOrderId.value = order.id
  editingStatusValue.value = ['paid', 'picked_up'].includes(order.order_status) ? order.order_status : 'pending_payment'
}

function cancelEditStatus() {
  editingStatusOrderId.value = null
  editingStatusResId.value = null
  editingStatusValue.value = ''
}

async function saveStatus(order) {
  if (order.order_status === 'paid' && editingStatusValue.value !== 'paid') {
    await ordersStore.revertPaidOrder(order.id, editingStatusValue.value)
  } else {
    await ordersStore.updateOrderStatus(order.id, editingStatusValue.value)
    await ordersStore.fetchAllOrders()
  }
  toast.show(i18n.t('orders.payStatusToast'))
  editingStatusOrderId.value = null
}

function startEditNotes(order) {
  editingNotesOrderId.value = order.id
  editingNotesValue.value = order.admin_notes || ''
}

function cancelEditNotes() {
  editingNotesOrderId.value = null
  editingNotesValue.value = ''
}

async function saveAdminNotes(order) {
  await ordersStore.updateAdminNotes(order.id, userStore.currentUser.id, editingNotesValue.value || null)
  toast.show(i18n.t('orders.saveNotesToast'))
  editingNotesOrderId.value = null
}

async function handleCancel(itemId) {
  await ordersStore.cancelOrderItem(itemId)
  toast.show(i18n.t('orders.cancelToast'))
}

const ORDER_STATUSES = ['待付訂金', '待入住', '已入住', '已退房', '已取消']

function resStatusLabel(status) {
  return i18n.t(`reservations.statusLabels.${status}`) || status
}

const editingStatusResId = ref(null)
const editingAdminNoteResId = ref(null)
const editingAdminNoteValue = ref('')

// ── Reservations filter, sort & pagination ────────────────────────────────────
const resStatusFilter = ref([])
const resSearchQuery = ref('')
const resCurrentPage = ref(1)
const resPageSize = 10
const resSortColumn = ref('id')
const resSortDirection = ref('desc')

function toggleResSort(col) {
  if (resSortColumn.value === col) {
    resSortDirection.value = resSortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    resSortColumn.value = col
    resSortDirection.value = 'asc'
  }
  resCurrentPage.value = 1
}

const filteredReservations = computed(() => {
  let list = reservationsStore.reservations
  if (resStatusFilter.value.length > 0) {
    list = list.filter(r => resStatusFilter.value.includes(r.order_status))
  }
  if (resSearchQuery.value) {
    const q = resSearchQuery.value.toLowerCase()
    list = list.filter(r =>
      (r.order_number || String(r.id)).toLowerCase().includes(q) ||
      (r.buyer_last_name || '').toLowerCase().includes(q) ||
      (r.buyer_first_name || '').toLowerCase().includes(q) ||
      (r.buyer_email || '').toLowerCase().includes(q)
    )
  }
  return [...list].sort((a, b) => {
    let aVal, bVal
    const dir = resSortDirection.value
    if (resSortColumn.value === 'id')        { aVal = a.id; bVal = b.id }
    else if (resSortColumn.value === 'check_in')  { aVal = a.check_in || ''; bVal = b.check_in || '' }
    else if (resSortColumn.value === 'check_out') { aVal = a.check_out || ''; bVal = b.check_out || '' }
    else if (resSortColumn.value === 'nights')    { aVal = a.nights ?? 0; bVal = b.nights ?? 0 }
    else if (resSortColumn.value === 'deposit')   { aVal = parseFloat(a.deposit_amount) || 0; bVal = parseFloat(b.deposit_amount) || 0 }
    else if (resSortColumn.value === 'total')     { aVal = parseFloat(a.total_price) || 0; bVal = parseFloat(b.total_price) || 0 }
    else if (resSortColumn.value === 'status')    { const rank = { '待付訂金': 0, '待入住': 1, '已入住': 2, '已退房': 3, '已取消': 4 }; aVal = rank[a.order_status] ?? 99; bVal = rank[b.order_status] ?? 99 }
    else if (resSortColumn.value === 'buyer')     { aVal = (a.buyer_last_name || '') + (a.buyer_first_name || ''); bVal = (b.buyer_last_name || '') + (b.buyer_first_name || '') }
    else if (resSortColumn.value === 'created')   { aVal = a.created_at || ''; bVal = b.created_at || '' }
    else if (resSortColumn.value === 'updated')   { aVal = a.updated_at || ''; bVal = b.updated_at || '' }
    else { aVal = a.id; bVal = b.id }
    if (aVal < bVal) return dir === 'asc' ? -1 : 1
    if (aVal > bVal) return dir === 'asc' ? 1 : -1
    return 0
  })
})
const resTotalPages = computed(() => Math.ceil(filteredReservations.value.length / resPageSize))
const resPaginatedReservations = computed(() => {
  const start = (resCurrentPage.value - 1) * resPageSize
  return filteredReservations.value.slice(start, start + resPageSize)
})
const resDtFrom = computed(() => filteredReservations.value.length === 0 ? 0 : (resCurrentPage.value - 1) * resPageSize + 1)
const resDtTo = computed(() => Math.min(resCurrentPage.value * resPageSize, filteredReservations.value.length))
const resPageNumbers = computed(() => {
  const total = resTotalPages.value
  const cur = resCurrentPage.value
  const range = []
  for (let i = Math.max(1, cur - 2); i <= Math.min(total, cur + 2); i++) range.push(i)
  return range
})

watch(resStatusFilter, () => { resCurrentPage.value = 1 }, { deep: true })
watch(resSearchQuery, () => { resCurrentPage.value = 1 })

function toggleResStatusFilter(s) {
  const idx = resStatusFilter.value.indexOf(s)
  resStatusFilter.value = idx === -1
    ? [...resStatusFilter.value, s]
    : resStatusFilter.value.filter(x => x !== s)
}

function orderStatusClass(status) {
  if (status === '已取消') return 'status-cancelled'
  if (status === '已退房') return 'status-paid'
  if (status === '已入住') return 'status-paid'
  if (status === '待入住') return 'status-paid'
  return 'status-unpaid'
}

function startEditResStatus(res) {
  editingStatusResId.value = res.id
  editingStatusValue.value = res.order_status
}
async function saveResStatus(res) {
  if (editingStatusValue.value && editingStatusValue.value !== res.order_status) {
    await reservationsStore.updateOrderStatus(res.id, editingStatusValue.value)
    await reservationsStore.fetchAllReservations()
    toast.show(i18n.t('reservations.statusUpdatedToast'))
  }
  editingStatusResId.value = null
}

function startEditAdminNote(res) {
  editingAdminNoteResId.value = res.id
  editingAdminNoteValue.value = res.admin_note || ''
}
function cancelEditAdminNote() {
  editingAdminNoteResId.value = null
  editingAdminNoteValue.value = ''
}
async function saveAdminNote(res) {
  await reservationsStore.updateAdminNote(res.id, editingAdminNoteValue.value)
  editingAdminNoteResId.value = null
  editingAdminNoteValue.value = ''
}

function reset() {
  ordersStore.clearOrders()
  reservationsStore.clearReservations()
  expandedOrderId.value = null
  expandedResId.value = null
  editingOrderId.value = null
  userStore.logout()
  form.value = { name: '', email: '', phone: '' }
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function statusLabel(order) {
  const map = { paid: i18n.t('orders.paid'), pending_payment: i18n.t('orders.pending_payment'), picked_up: i18n.t('orders.picked_up'), cancelled: i18n.t('orders.cancelled') }
  return map[order.order_status] || order.order_status
}

function statusClass(order) {
  if (order.order_status === 'paid') return 'status-paid'
  if (order.order_status === 'picked_up') return 'status-paid'
  if (order.order_status === 'cancelled') return 'status-cancelled'
  return 'status-unpaid'
}

function activeItemCount(order) {
  return order.items.filter(i => i.status !== 'cancelled' && i.status !== 'sold').length
}

function orderTotal(order) {
  return order.items
    .filter(i => i.status !== 'cancelled' && i.status !== 'sold')
    .reduce((s, i) => s + i.price, 0)
    .toFixed(2)
    .replace(/\.00$/, '')
}

function orderOriginalTotal(order) {
  return order.items
    .filter(i => i.status !== 'cancelled' && i.status !== 'sold')
    .reduce((s, i) => s + (i.original_price || i.price), 0)
    .toFixed(2)
    .replace(/\.00$/, '')
}

function hasDiscount(order) {
  return order.items.some(i => i.status !== 'cancelled' && i.status !== 'sold' && i.original_price && i.original_price > i.price)
}

function hasNotFirstPosition(order) {
  return order.items.some(i => i.status === 'reserved' && i.waiting_position > 1)
}

function isAllSoldCancelled(order) {
  return order.order_status === 'cancelled' && order.items.some(i => i.status === 'sold')
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const [year, month, day] = dateStr.split('-')
  return `${month}/${day}/${year}`
}

function formatDateTime(isoStr) {
  if (!isoStr) return '—'
  const d = new Date(isoStr)
  const date = `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
  const h = d.getHours()
  const ampm = h >= 12 ? 'PM' : 'AM'
  const h12 = h % 12 || 12
  const time = `${h12}:${String(d.getMinutes()).padStart(2, '0')} ${ampm}`
  return `${date} ${time}`
}

function toPickerFormat(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const year = d.getFullYear()
  const hour = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${month}/${day}/${year} ${hour}:${min}`
}

function fromPickerFormat(str) {
  if (!str) return null
  const parts = str.match(/(\d+)\/(\d+)\/(\d+)\s+(\d+):(\d+)/)
  if (!parts) return null
  return new Date(+parts[3], +parts[1] - 1, +parts[2], +parts[4], +parts[5]).toISOString()
}

// ── Pickup/Rental Calendar ────────────────────────────────────────────────────
const calSelectedItem = ref(null)
const calHoverResId = ref(null)
const calYear = ref(new Date().getFullYear())
const calMonth = ref(new Date().getMonth())

const calMonthLabel = computed(() => {
  const d = new Date(calYear.value, calMonth.value, 1)
  return d.toLocaleString('en-US', { month: 'long', year: 'numeric' })
})

function calPrevMonth() {
  if (calMonth.value === 0) { calMonth.value = 11; calYear.value-- }
  else calMonth.value--
}

function calNextMonth() {
  if (calMonth.value === 11) { calMonth.value = 0; calYear.value++ }
  else calMonth.value++
}

function calFormatTime(isoStr) {
  const d = new Date(isoStr)
  const h = d.getHours()
  const ampm = h >= 12 ? 'PM' : 'AM'
  const h12 = h % 12 || 12
  const min = d.getMinutes()
  return min === 0 ? `${h12}${ampm}` : `${h12}:${String(min).padStart(2, '0')}${ampm}`
}

const calCells = computed(() => {
  const year = calYear.value
  const month = calMonth.value
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const prevMonthDays = new Date(year, month, 0).getDate()
  const today = new Date()
  const paidOrders = ordersStore.orders.filter(o => o.order_status === 'paid' && o.pickup_time)
  const activeReservations = reservationsStore.reservations.filter(r =>
    ['待入住', '已入住', '已退房'].includes(r.order_status) && r.check_in && r.check_out
  )
  const cells = []

  for (let i = firstDay - 1; i >= 0; i--) {
    cells.push({ key: `prev-${i}`, day: prevMonthDays - i, inMonth: false, isToday: false, events: [] })
  }

  for (let d = 1; d <= daysInMonth; d++) {
    const isToday = today.getFullYear() === year && today.getMonth() === month && today.getDate() === d
    const cellDateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`

    const orderEvents = paidOrders
      .filter(o => {
        const pt = new Date(o.pickup_time)
        return pt.getFullYear() === year && pt.getMonth() === month && pt.getDate() === d
      })
      .sort((a, b) => new Date(a.pickup_time) - new Date(b.pickup_time))
      .map(o => {
        const timeStr = calFormatTime(o.pickup_time)
        const buyerName = `${o.buyer_last_name || ''} ${o.buyer_first_name || ''}`.trim()
        const fullLabel = `${timeStr}-${o.order_number}-${buyerName}`
        return { id: `order-${o.id}`, label: fullLabel, fullLabel, type: 'order', data: o }
      })

    const dayOfWeek = (firstDay + d - 1) % 7  // 0=Sun, 6=Sat
    const resEvents = activeReservations
      .filter(r => cellDateStr >= r.check_in && cellDateStr <= r.check_out)
      .map(r => {
        const isStart = cellDateStr === r.check_in
        const isEnd = cellDateStr === r.check_out
        const visualStart = isStart || dayOfWeek === 0
        const visualEnd = isEnd || dayOfWeek === 6
        let spanPos
        if (visualStart && visualEnd) spanPos = 'only'
        else if (visualStart) spanPos = 'start'
        else if (visualEnd) spanPos = 'end'
        else spanPos = 'mid'
        const buyerName = `${r.buyer_last_name || ''} ${r.buyer_first_name || ''}`.trim()
        const fullLabel = `${r.order_number || r.id}-${buyerName}`
        return { id: `res-${r.id}`, label: isStart ? fullLabel : '', fullLabel, type: 'reservation', data: r, spanPos }
      })

    cells.push({ key: `day-${d}`, day: d, inMonth: true, isToday, events: [...orderEvents, ...resEvents] })
  }

  const remaining = (7 - (cells.length % 7)) % 7
  for (let i = 1; i <= remaining; i++) {
    cells.push({ key: `next-${i}`, day: i, inMonth: false, isToday: false, events: [] })
  }

  return cells
})
</script>

<style scoped>
/* ── Lookup form ─────────────────────────────────────────────────────────── */
.orders-lookup {
  max-width: 380px; margin: 40px auto; text-align: center;
}
.lookup-title {
  font-family: var(--font-display);
  font-size: 1.2rem; margin-bottom: 24px;
  color: var(--charcoal);
}
.error-msg {
  margin-top: 10px; font-size: 0.8rem; color: var(--red);
}
.field-error {
  margin-top: 4px; font-size: 0.75rem; color: var(--red); text-align: left;
}
.input-error { border-color: var(--red) !important; }

/* ── No orders ───────────────────────────────────────────────────────────── */
.no-orders-state {
  text-align: center; padding: 60px 20px; color: var(--mid);
}
.greeting { font-size: 1rem; }

/* ── Orders greeting ─────────────────────────────────────────────────────── */
.orders-greeting {
  font-size: 1rem; font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 8px;
}
.orders-section-title {
  font-size: 1.25rem; font-weight: 700;
  color: var(--charcoal);
  margin-bottom: 16px;
}

/* ── Orders table ────────────────────────────────────────────────────────── */
.orders-table-wrap {
  width: 100%;
}
.table-scroll-wrap {
  width: 100%; overflow-x: auto;
}
.orders-table {
  width: 100%; border-collapse: collapse;
  font-size: 0.88rem;
}
.orders-table thead tr {
  border-bottom: 2px solid var(--border);
}
.orders-table th {
  text-align: left; padding: 8px 12px;
  font-size: 0.82rem; font-weight: 600; color: var(--mid);
  white-space: nowrap;
}
.order-row {
  cursor: pointer; border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}
.order-row:hover { background: #edf4f4; }
.order-row.expanded {
  background: #edf4f4;
  border-bottom: none;
  font-weight: 600;
}
.orders-table td {
  padding: 10px 12px; vertical-align: middle;
}
.td-order-no { font-weight: 600; color: var(--charcoal); }

/* Payment status */
.status-paid      { color: #2e7d32; font-weight: 600; }
.status-unpaid    { color: var(--mid); }
.status-cancelled { color: var(--red, #c0392b); }

/* All-sold cancelled order row */
.order-row-dimmed { background: #d9d9d9 !important; color: var(--mid); }
.order-row-dimmed:hover { background: #edf4f4 !important; }

/* No pickup available */
.no-pickup-text { color: var(--mid); font-style: italic; }

/* All sold out note */
.all-sold-note { color: var(--red, #c0392b); font-size: 0.78rem; font-weight: 600; margin-left: 6px; }

/* Admin buyer columns */
.td-buyer      { white-space: nowrap; font-size: 0.82rem; }
.td-buyer-info { white-space: nowrap; font-size: 0.78rem; color: var(--mid); }

/* Admin notes column */
.td-admin-notes { min-width: 140px; max-width: 240px; font-size: 0.78rem; color: var(--mid); }
.notes-display  { display: inline-flex; align-items: center; gap: 4px; }
.notes-text     { white-space: pre-wrap; word-break: break-word; }
.notes-edit-wrap { display: flex; flex-direction: column; gap: 6px; }
.notes-textarea {
  width: 100%; min-width: 160px; font-family: var(--font-body); font-size: 0.8rem;
  border: 1.5px solid var(--border); border-radius: var(--radius);
  padding: 4px 8px; color: var(--charcoal); background: #fff;
  outline: none; resize: vertical;
}
.notes-textarea:focus { border-color: var(--charcoal); }

/* Pickup time cell */
.td-pickup { white-space: nowrap; }
.td-created { white-space: nowrap; color: var(--mid); font-size: 0.82rem; }
.btn-edit-icon {
  background: none; border: none; cursor: pointer;
  color: var(--accent); padding: 2px 4px; margin-left: 4px;
  border-radius: 3px; vertical-align: middle;
  transition: opacity 0.15s;
}
.btn-edit-icon:hover { opacity: 0.7; }

.status-display {
  display: inline-flex; align-items: center; white-space: nowrap;
}

/* Inline status edit */
.status-edit-wrap {
  display: flex; flex-direction: column; gap: 6px;
}
.status-select {
  font-family: var(--font-body); font-size: 0.8rem;
  border: 1.5px solid var(--border); border-radius: var(--radius);
  padding: 4px 8px; color: var(--charcoal);
  background: #fff; outline: none;
  cursor: pointer;
}
.status-select:focus { border-color: var(--charcoal); }

/* Inline pickup edit */
.pickup-edit-wrap {
  display: flex; flex-direction: column; gap: 6px; min-width: 220px;
}
.pickup-edit-actions {
  display: flex; gap: 6px;
}
.btn-save-pickup {
  padding: 4px 12px; background: var(--charcoal); color: #fff;
  border: none; border-radius: var(--radius); font-size: 0.78rem;
  cursor: pointer; transition: opacity 0.15s;
}
.btn-save-pickup:hover { opacity: 0.8; }
.btn-cancel-pickup {
  padding: 4px 10px; background: none; color: var(--mid);
  border: 1px solid var(--border); border-radius: var(--radius);
  font-size: 0.78rem; cursor: pointer;
}
.btn-cancel-pickup:hover { border-color: var(--charcoal); color: var(--charcoal); }

/* ── Expand row ──────────────────────────────────────────────────────────── */
.expand-row > td {
  padding: 0;
  background: #fff;
  border-top: 1px solid var(--border);    
  border-top: 1.5px solid #858585;
  border-bottom: 1.5px solid #858585;
}

/* ── Order summary ───────────────────────────────────────────────────────── */
.order-summary {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; border-top: 1px solid var(--border);
  font-size: 0.88rem; font-weight: 600;
}
.summary-price { display: flex; align-items: center; gap: 6px; }
.strikethrough {
  text-decoration: line-through; color: var(--mid); font-weight: 400;
  font-size: 0.82rem;
}
.not-first-warning {
  margin: 0; padding: 8px 16px 12px;
  color: var(--red, #c0392b); font-size: 0.8rem; font-weight: 600;
}

/* ── Empty table state ───────────────────────────────────────────────────── */
.td-empty {
  text-align: center; padding: 24px 12px;
  color: var(--mid); font-size: 0.88rem; font-style: italic;
}

/* ── Reservations section ────────────────────────────────────────────────── */
.reservations-section {
  width: 100%; margin-top: 32px;
}
.reservations-section-title {
  margin-top: 0;
}
.reservations-table tbody tr.order-row:hover { background: #edf4f4; }
.reservations-table tbody tr.order-row { cursor: pointer; }

/* ── Reservation expand ──────────────────────────────────────────────────── */
.res-expand-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px 24px;
  padding: 14px 16px;
  background: #fff;
}
.res-detail-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.res-detail-cell--span3 {
  grid-column: span 3;
}
.res-detail-label {
  color: var(--mid);
  font-size: 0.75rem;
  word-break: break-word;
}
.res-detail-value {
  color: var(--charcoal);
  font-size: 0.88rem;
  font-weight: 500;
  word-break: break-word;
}

/* ── Shopping guide ──────────────────────────────────────────────────────── */
.shopping-guide-wrap {
  width: 100%; margin-top: 24px;
  border-top: 1.5px solid var(--border); padding-top: 16px;
}
.guide-toggle-btn {
  display: flex; align-items: center; justify-content: space-between;
  width: 100%; background: none; border: none; cursor: pointer;
  font-size: 1.2rem; font-weight: 700; color: var(--charcoal);
  padding: 8px 10px; margin: 0 -10px; width: calc(100% + 20px);
  text-align: left; border-radius: var(--radius);
  transition: background 0.15s, color 0.15s;
}
.guide-toggle-btn:hover {
  background: #edf4f4;
}
.guide-collapse-body { margin-top: 12px; }
.rent-guide-content { font-size: .9rem; color: #444; line-height: 1.6; }
.rent-guide-content :deep(ul), .rent-guide-content :deep(ol) { padding-left: 1.5em; }
.rent-guide-content :deep(ul) { list-style-type: disc; }
.rent-guide-content :deep(ol) { list-style-type: decimal; }
.rent-guide-content :deep(ul ul) { list-style-type: circle; }
.rent-guide-content :deep(ul ul ul) { list-style-type: square; }
.rent-guide-content :deep(blockquote) { margin-left: 1.5em; padding-left: 0.75em; border-left: 3px solid var(--border); }
.rent-guide-content :deep(iframe) { width: 100% !important; max-width: 100%; height: 360px; border: none; border-radius: 6px; display: block; margin: 8px 0; }
.rent-guide-content :deep(.map-embed) { width: 100%; }
.rent-guide-empty { font-size: 0.82rem; color: var(--mid); font-style: italic; }

/* ── Mark paid button (admin) ────────────────────────────────────────────── */
.btn-mark-paid {
  margin-left: 6px; padding: 2px 8px;
  background: none; border: 1px solid currentColor; border-radius: var(--radius);
  font-size: 0.72rem; color: inherit; cursor: pointer;
  transition: opacity 0.15s;
}
.btn-mark-paid:hover { opacity: 0.7; }

/* ── Back button ─────────────────────────────────────────────────────────── */
.back-btn-wrap { display: flex; justify-content: center; margin-top: 16px; }
.back-btn { display: inline-flex; align-items: center; gap: 5px; }

/* ── DataTable toolbar ───────────────────────────────────────────────────── */
.dt-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px; gap: 12px; flex-wrap: wrap;
}
.dt-info {
  font-size: 0.78rem; color: var(--mid);
}
.dt-search {
  padding: 5px 10px; border: 1px solid var(--border); border-radius: var(--radius);
  font-size: 0.82rem; color: var(--charcoal); background: #fff;
  outline: none; min-width: 180px;
}
.dt-search:focus { border-color: var(--charcoal); }
.dt-status-filters {
  display: flex; gap: 6px; flex-wrap: wrap;
}
.dt-filter-btn {
  padding: 4px 12px; border: 1px solid var(--border); border-radius: var(--radius);
  font-size: 0.78rem; cursor: pointer; background: #fff; color: var(--charcoal);
  transition: background 0.15s, border-color 0.15s;
}
.dt-filter-btn:hover { border-color: var(--charcoal); }
.dt-filter-btn.active { background: var(--charcoal); color: #fff; border-color: var(--charcoal); }

/* ── Sortable headers ────────────────────────────────────────────────────── */
.orders-table th.sortable {
  cursor: pointer; user-select: none;
}
.orders-table th.sortable:hover { color: var(--charcoal); }
.sort-icon {
  display: inline-flex; vertical-align: middle;
  margin-left: 3px; opacity: 0.6;
}

/* ── Pagination ──────────────────────────────────────────────────────────── */
.dt-pagination {
  display: flex; align-items: center; justify-content: flex-end;
  gap: 4px; margin-top: 12px; flex-wrap: wrap;
}
.dt-page-btn {
  padding: 4px 10px; border: 1px solid var(--border); border-radius: var(--radius);
  background: #fff; font-size: 0.8rem; color: var(--charcoal);
  cursor: pointer; transition: background 0.12s, border-color 0.12s;
  min-width: 32px; text-align: center;
}
.dt-page-btn:hover:not(:disabled):not(.active) { border-color: var(--charcoal); }
.dt-page-btn.active {
  background: var(--charcoal); color: #fff; border-color: var(--charcoal);
}
.dt-page-btn:disabled { opacity: 0.35; cursor: default; }

/* ── Pickup/Rental Calendar ──────────────────────────────────────────────── */
.pickup-calendar-section {
  margin-top: 32px;
}
.cal-nav {
  display: flex; align-items: center; gap: 14px; margin-bottom: 12px;
}
.cal-nav-btn {
  background: none; border: 1px solid var(--border); border-radius: 4px;
  padding: 2px 12px; cursor: pointer; font-size: 1.1rem; color: var(--charcoal);
  transition: border-color 0.15s;
}
.cal-nav-btn:hover { border-color: var(--charcoal); }
.cal-month-label { font-weight: 600; font-size: 1rem; color: var(--charcoal); }
.cal-grid {
  display: grid; grid-template-columns: repeat(7, 1fr);
  border: 1px solid var(--border); border-radius: 6px; overflow: hidden;
}
.cal-day-header {
  background: #f5f3f0; padding: 6px 4px; text-align: center;
  font-size: 0.75rem; font-weight: 600; color: var(--mid);
  border-bottom: 1px solid var(--border);
  border-right: 1px solid var(--border);
}
.cal-day-header:last-child { border-right: none; }
.cal-day {
  min-height: 80px; padding: 4px 5px; border-right: 1px solid var(--border);
  border-bottom: 1px solid var(--border); vertical-align: top;
  background: #fff; overflow: hidden;
}
.cal-day:nth-child(7n) { border-right: none; }
.cal-day--other { background: #faf9f7; }
.cal-day-num {
  font-size: 0.75rem; font-weight: 600; color: var(--charcoal);
  margin-bottom: 3px; width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
}
.cal-day-num--today {
  background: var(--accent); color: #fff; border-radius: 50%;
}
.cal-day--other .cal-day-num { color: var(--mid); }
.cal-event {
  background: var(--accent-light); color: var(--charcoal);
  border-radius: 3px; padding: 2px 5px; margin-bottom: 2px;
  font-size: 0.8rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  cursor: pointer; max-width: 100%;
}
.cal-event:hover { opacity: 0.85; }
.cal-event--reservation:hover { opacity: 1; }
.cal-event--res-hovered { background: #a8cfa3 !important; color: #1a4016 !important; }
.cal-event--reservation {
  background: #d4e8d0; color: #2e5e28;
  min-height: 1.5rem; text-align: center; align-items: center;
}
.cal-event--span-start { border-radius: 10px 0 0 10px; }
.cal-event--span-mid   { border-radius: 0; }
.cal-event--span-end   { border-radius: 0 10px 10px 0; }
.cal-event--span-only  { border-radius: 3px; }

/* ── Calendar order modal ────────────────────────────────────────────────── */
.cal-modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  z-index: 1000; display: flex; align-items: center; justify-content: center;
  padding: 20px;
}
.cal-modal {
  background: #fff; border-radius: 8px; width: 100%; max-width: 620px;
  max-height: 85vh; display: flex; flex-direction: column;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
}
.cal-modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px; border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.cal-modal-title {
  font-size: 1rem; font-weight: 700; color: var(--charcoal);
}
.cal-modal-close {
  background: none; border: none; cursor: pointer; font-size: 1rem;
  color: var(--mid); padding: 2px 6px; border-radius: 4px;
  transition: color 0.15s;
}
.cal-modal-close:hover { color: var(--charcoal); }
.cal-modal-body {
  padding: 16px 20px; overflow-y: auto; flex: 1;
}
.cal-modal-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px 20px;
  margin-bottom: 16px;
}
.cal-modal-field {
  display: flex; flex-direction: column; gap: 2px;
}
.cal-modal-field--full {
  grid-column: span 2;
}
.cal-modal-label {
  font-size: 0.72rem; color: var(--mid); font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.03em;
}
.cal-modal-notes {
  white-space: pre-wrap; word-break: break-word; font-size: 0.88rem;
}
.cal-modal-items-title {
  font-size: 0.82rem; font-weight: 600; color: var(--mid);
  margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid var(--border);
}
</style>
