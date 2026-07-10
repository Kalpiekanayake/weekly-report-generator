export const Card = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white p-6 rounded-xl shadow-sm border border-gray-100 ${className}`}>
    {children}
  </div>
);
