interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export const Input = ({ label, ...props }: InputProps) => (
  <div className="mb-4">
    <label className="block text-sm font-medium text-gray-700">{label}</label>
    <input
      {...props}
      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
    />
  </div>
);
