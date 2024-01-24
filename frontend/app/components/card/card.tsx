import styles from "./card.module.scss";
import classNames from "classnames";

const Card = ({
    children,
    title,
    subtitle,
    nowrap,
    className,
}: {
    children: React.ReactNode;
    title: string;
    subtitle?: string;
    nowrap?: boolean;
    className?: string | string[];
}) => {
    const cardStyle = classNames(styles.card, className);

    return (
        <div className={cardStyle}>
            <div className={styles.headingContainer}>
                <h3 className={styles.title}>{title}</h3>
                {subtitle ? (
                    <h4 className={styles.subtitle}>{subtitle}</h4>
                ) : null}
            </div>
            <div className={nowrap ? undefined : styles.cardBodyWrap}>
                {children}
            </div>
        </div>
    );
};

export default Card;
