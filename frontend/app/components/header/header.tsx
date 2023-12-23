import styles from "./header.module.scss"


export type NavLinks = {
    label: string;
    path: string;
}

export type HeaderProps = {
    nav_links: NavLinks[];
}

const Header = ({nav_links}: HeaderProps) => {
    return (
        <header>
            <div className={styles.top_header_container}>
                <h1>Top 500 Aggregator</h1>
            </div>

            <div className={styles.navbar}>
                <ul>
                    {nav_links.map(link => {
                        return <li><a href={link.path}>{link.label}</a></li>
                    })}

                </ul>
            </div>

        </header>
    )
}
export default Header