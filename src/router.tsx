import React from 'react'
import { createRouter, createRoute, createRootRoute, Outlet } from '@tanstack/react-router'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { queryClient } from '@/lib/queryClient'
import Home from '@/app/page'
import { z } from 'zod'
import '@/app/globals.css'

export const venueSearchSchema = z.object({
  vibe: z.string().optional().catch('all'),
  price_range: z.string().optional().catch('all'),
  category: z.string().optional(),
})

export type VenueSearch = z.infer<typeof venueSearchSchema>

const rootRoute = createRootRoute({
  component: () => (
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <Outlet />
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </React.StrictMode>
  ),
})

export const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  validateSearch: (search: Record<string, unknown>) => venueSearchSchema.parse(search),
  component: Home,
})

const routeTree = rootRoute.addChildren([indexRoute])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
