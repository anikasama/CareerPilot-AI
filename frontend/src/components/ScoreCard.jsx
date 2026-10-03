export default function ScoreCard({
  label,
  score,
  description,
  icon,
}) {
  return (
    <div className="score-card">
      <div className="score-card-top">
        <div className="score-icon">
          {icon}
        </div>

        <span className="score-label">
          {label}
        </span>
      </div>

      <div className="score-number">
        {score}
        <span>/100</span>
      </div>

      <p>{description}</p>
    </div>
  );
}