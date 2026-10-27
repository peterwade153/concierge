import type { RestaurantRecommendations } from "../api/types";
import { SpotCard } from "./SpotCard";

interface RecommendationViewProps {
  data: RestaurantRecommendations;
}

export function RecommendationView({ data }: RecommendationViewProps) {
  return (
    <section className="space-y-5">
      <div className="rounded-xl border border-brand-100 bg-brand-50 px-5 py-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-brand-600">
          Neighborhood searched
        </p>
        <h2 className="mt-1 text-xl font-bold text-brand-900">
          {data.neighborhood_searched}
        </h2>
        <p className="mt-2 text-sm text-slate-600">{data.summary_verdict}</p>
      </div>

      {data.recommended_spots && data.recommended_spots.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {data.recommended_spots.map((spot) => (
            <SpotCard key={spot.name} spot={spot} />
          ))}
        </div>
      ) : (
        <p className="text-center text-sm text-slate-400">
          No recommendations were found for this area.
        </p>
      )}
    </section>
  );
}