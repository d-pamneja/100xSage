import { Card, CardContent } from "@/components/ui/card";

const CardGrid = () => {
  return (
    <div className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-3">
      <Card className="bg-gray-900 p-6 text-white">
        <CardContent>
          <h3 className="text-xl font-semibold">⚡ Instant AI Responses</h3>
          <p className="mt-2 text-gray-400">
            No more waiting for TAs - AI handles common questions instantly.
          </p>
        </CardContent>
      </Card>
      <Card className="bg-gray-900 p-6 text-white">
        <CardContent>
          <h3 className="text-xl font-semibold">📊 Live Insights</h3>
          <p className="mt-2 text-gray-400">
            Track student queries and discover trending topics in real-time.
          </p>
        </CardContent>
      </Card>
      <Card className="bg-gray-900 px-5 pt-6 text-white">
        <CardContent>
          <h3 className="text-xl font-semibold">🎯 Performance Analytics</h3>
          <p className="mt-2 text-gray-400">
            Identify top-performing TAs and monitor response quality.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default CardGrid;
