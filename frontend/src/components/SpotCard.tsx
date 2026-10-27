import type { RestaurantDetails } from "../api/types";

interface SpotCardProps {
  spot: RestaurantDetails;
}

function formatRating(rating: number | null): string {
  if (rating == null) return "Unrated";
  return rating.toFixed(1);
}

export function SpotCard({ spot }: SpotCardProps) {
  return (
    <article className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md">
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-lg font-semibold text-brand-900">{spot.name}</h3>
        {spot.rating != null && (
          <span
            aria-label={`Rating ${formatRating(spot.rating)} out of 5`}
            className="shrink-0 rounded-full bg-brand-50 px-2.5 py-1 text-xs font-semibold text-brand-700"
          >
            ★ {formatRating(spot.rating)}
          </span>
        )}
      </div>

      <p className="text-sm text-slate-500">{spot.location}</p>

      {spot.cuisine && spot.cuisine.length > 0 && (
        <ul className="flex flex-wrap gap-1.5">
          {spot.cuisine.map((cuisine) => (
            <li
              key={cuisine}
              className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600"
            >
              {cuisine}
            </li>
          ))}
        </ul>
      )}

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-slate-500">
        {spot.price_range && (
          <span className="font-medium text-slate-700">{spot.price_range}</span>
        )}
      </div>

      {spot.specialty && (
        <p className="text-sm italic text-slate-500">{spot.specialty}</p>
      )}
    </article>
  );
}