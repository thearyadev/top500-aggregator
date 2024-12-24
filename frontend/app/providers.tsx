'use client'
import posthog from 'posthog-js'
import { PostHogProvider } from 'posthog-js/react'

if (typeof window !== 'undefined') {
    posthog.init("phc_OfKo0jrYcH80kqAbXxq5fM0WbTIoOOFWdP8Mv4WKDyQ", {
        api_host: "https://us.i.posthog.com",
        person_profiles: 'always',
    })
}
export function CSPostHogProvider({ children }: { children: React.ReactNode }) {
    return <PostHogProvider client={posthog}>{children}</PostHogProvider>
}
