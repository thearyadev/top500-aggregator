import styles from "./card.module.scss"


const Card = ({children, title, subtitle}: { children: React.ReactNode, title: string, subtitle?: string }) => {
    return (
        <div className={styles.card}>
            <div className={styles.headingContainer}>
                <h3 className={styles.title}>{title}</h3>
                {subtitle ? <h4 className={styles.subtitle}>{subtitle}</h4> : null}
            </div>
            <hr  className="m-4"/>
            <div className={styles.cardBody}>
                {children}
            </div>
        </div>
    )
}

export default Card;