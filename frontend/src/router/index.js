import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/authStore"

// Public
import LoginView from "@/views/LoginView.vue"
import RegisterView from "@/views/RegisterView.vue"

// User Views
import UserDashboard from "@/views/UserDashboard.vue"
import LotsView from "@/views/LotsView.vue"
import SpotsView from "@/views/SpotsView.vue"
import BookingsView from "@/views/BookingsView.vue"

// Admin Views
import AdminDashboard from "@/views/AdminDashboard.vue"
import AdminLots from "@/views/AdminLots.vue"
import AdminSpots from "@/views/AdminSpots.vue"
import AdminUsers from "@/views/AdminUsers.vue"
import AdminBookings from "@/views/AdminBookings.vue"
import AdminCharts from "@/views/AdminCharts.vue"
import UserChart from "@/views/UserCharts.vue"


// Misc
import NotFound from "@/views/NotFound.vue"

const routes = [
  { path: "/", name: "login", component: LoginView },
  { path: "/register", name: "register", component: RegisterView },

  // USER ROUTES
  { path: "/user/dashboard", component: UserDashboard, meta: { requiresAuth: true, role: "user" }},
  { path: "/user/lots", component: LotsView, meta: { requiresAuth: true, role: "user" }},
  { path: "/user/spots/:lotId", component: SpotsView, meta: { requiresAuth: true, role: "user" }},
  { path: "/user/bookings", component: BookingsView, meta: { requiresAuth: true, role: "user" }},
  { path: "/user/charts", name: "UserCharts", component: UserChart, meta: { requiresAuth: true, role: "user" }},

  // ADMIN ROUTES
  { path: "/admin/dashboard", component: AdminDashboard, meta: { requiresAuth: true, role: "admin" }},
  { path: "/admin/lots", component: AdminLots, meta: { requiresAuth: true, role: "admin" }},
  { path: "/admin/spots/:lotId", component: AdminSpots,name: "AdminSpots", meta: { requiresAuth: true, role: "admin" }},
  { path: "/admin/users", component: AdminUsers, meta: { requiresAuth: true, role: "admin" }},
  { path: "/admin/bookings", component: AdminBookings, meta: { requiresAuth: true, role: "admin" }},
  { path: "/admin/charts", component: AdminCharts, meta: { requiresAuth: true, role: "admin" }},

  { path: "/:pathMatch(.*)*", name: "notFound", component: NotFound }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Route Guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.user) {
    return next("/")
  }

  if (to.meta.role && to.meta.role !== auth.role) {
    return next("/")
  }

  next()
})

export default router

