export const ErrorAlert = ({ message }: { message: string | string[] }) => {
  const messages = Array.isArray(message) ? message : [message];
  
  return (
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {messages.map((msg, index) => (
        <div key={index}>{msg}</div>
      ))}
    </div>
  );
};
