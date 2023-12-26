"use client";
import {useEffect, useState} from "react";
import styles from "./header.module.scss"
import {fetchSeasonList} from "@/app/utils/clientSideFetch";
import {useRouter} from "next/router";

type NavLinks = {
    label: string;
    path: string
}

const Header = () => {
    const [navLinks, setNavLinks] = useState<NavLinks[]>([])
    const router = useRouter();
    useEffect(() => {
        fetchSeasonList().then(seasonList => {
            setNavLinks(seasonList.reverse().map(season => {
                const seasonNumber = season.split("_")[0]
                return {label: `Season ${seasonNumber}`, path: `/season/${seasonNumber}`}
            }))
            if (router.pathname === "/" && typeof window !== undefined) {
                const element = document.getElementById("curseason")
                if (element) {
                    element.innerText = `Season ${seasonList[0].split("_")[0]}`
                }
            }

            if (typeof window !== undefined){
                const element = document.getElementById('navbar')
                if (element){
                    element.addEventListener('wheel', function(e) {
                        // @ts-ignore
                        if (e.deltaY != 0) {
                            // @ts-ignore
                            this.scrollLeft += (e.deltaY * 1.5);
                            e.preventDefault();
                        }
                    }, false);
                }

            }

        })

    }, []);


    return (
        <header>
            <div className={styles.top_header_container}>
                <h1>Top 500 Aggregator</h1>
            </div>

            <div className={styles.navbar} id="navbar">
                <ul>
                    {!!navLinks.length && navLinks.map(link => {
                        return <li><a className="block p-2 text-inherit no-underline" href={link.path}>{link.label}</a></li>
                    })}

                    {!navLinks.length && <li><p className="invisible">you're not supposed to see this...</p></li>}

                </ul>
            </div>

        </header>
    )
}
export default Header