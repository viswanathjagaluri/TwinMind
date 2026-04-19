export default function ListeningAnimation() {
    return (
        <div className="flex items-center gap-1">

            {[...Array(5)].map((_, i) => (
                <div
                    key={i}
                    className="w-1 bg-white rounded animate-wave"
                    style={{
                        height: `${10 + i * 4}px`,
                        animationDelay: `${i * 0.15}s`
                    }}
                />
            ))}

        </div>
    );
}