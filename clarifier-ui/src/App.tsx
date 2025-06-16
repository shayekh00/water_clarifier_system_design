import { useEffect, useState } from "react";

export default function ClarifierImageFilter() {
  const [images, setImages] = useState([]);
  const [minClarifiers, setMinClarifiers] = useState(0);
  const [maxClarifiers, setMaxClarifiers] = useState(10);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch(`http://localhost:8000/clarifiers?min=${minClarifiers}&max=${maxClarifiers}`);
      const data = await res.json();
      setImages(data);
    };
    fetchData();
  }, [minClarifiers, maxClarifiers]);

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <div className="flex gap-4 mb-6 items-end">
        <div>
          <label htmlFor="min" className="block text-sm font-medium">Min Clarifiers</label>
          <input
            id="min"
            type="number"
            className="border rounded px-2 py-1 w-full"
            value={minClarifiers}
            onChange={(e) => setMinClarifiers(Number(e.target.value))}
          />
        </div>
        <div>
          <label htmlFor="max" className="block text-sm font-medium">Max Clarifiers</label>
          <input
            id="max"
            type="number"
            className="border rounded px-2 py-1 w-full"
            value={maxClarifiers}
            onChange={(e) => setMaxClarifiers(Number(e.target.value))}
          />
        </div>
        <p className="text-muted-foreground ml-auto">{images.length} matches</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {images.map((item, idx) => (
          <div key={idx} className="border rounded-xl overflow-hidden shadow">
            <img
              src={`facility_images_azure/${item.image}`}
              alt={`Clarifiers in ${item.image}`}
              className="w-full h-24 object-cover rounded"
              style={{ height: '216px' }}
            />
            <div className="p-2">
              <p className="text-sm">
                <strong>Clarifiers:</strong> {item.clarifier_count}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
