import Link from "next/link";
import styles from "./header.module.scss";
import { get_season_list } from "@/app/server/actions";

type NavLinks = {
    label: string;
    path: string;
};

const Header = async () => {
    const seasons = await get_season_list();
    const navLinks: NavLinks[] = seasons.reverse().map((seasonNum) => {
        return { label: `Season ${seasonNum}`, path: `/season/${seasonNum}` };
    });
    navLinks.unshift({ label: "Trends", path: "/trends" });
    return (
        <header className="overflow-x-hidden">
            <div className={styles.top_header_container}>
                <Link href="/">
                    <h1>Top 500 Aggregator</h1>
                </Link>
            </div>

            <div className={styles.navbar} id="navbar">
                <ul>
                    {!!navLinks.length &&
                        navLinks.map((link) => {
                            return (
                                <li>
                                    <a
                                        className="block p-2 text-inherit no-underline"
                                        href={link.path}
                                    >
                                        {link.label}
                                    </a>
                                </li>
                            );
                        })}

                    {!navLinks.length && (
                        <li>
                            <p className="invisible">
                                you're not supposed to see this...
                            </p>
                        </li>
                    )}
                </ul>
            </div>
        </header>
    );
};
export default Header;
