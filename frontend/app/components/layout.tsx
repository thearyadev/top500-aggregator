import {Header} from "@/app/components/index";


export default function Layout({ children }: {children: React.ReactNode}) {
    return (
        <>
            <main>{children}</main>
        </>
    )
}