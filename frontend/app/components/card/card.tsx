import styles from "./card.module.scss";

const Card = ({
  children,
  title,
  subtitle,
  nowrap,
}: {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  nowrap?: boolean;
}) => {
  return (
    <div className={styles.card}>
      <div className={styles.headingContainer}>
        <h3 className={styles.title}>{title}</h3>
        {subtitle ? <h4 className={styles.subtitle}>{subtitle}</h4> : null}
      </div>
      <div className={nowrap ? undefined : styles.cardBodyWrap}>{children}</div>
    </div>
  );
};

export default Card;
