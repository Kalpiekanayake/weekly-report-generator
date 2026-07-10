interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  as?: React.ElementType;
  to?: string;
}

export const Button = ({ children, variant = 'primary', as: Component = 'button', ...props }: ButtonProps) => {
  const baseClasses = "px-4 py-2 rounded-lg font-medium transition duration-150 ease-in-out hover:scale-105 active:scale-95 disabled:opacity-50 disabled:hover:scale-100 flex items-center justify-center";
  const variants = {
    primary: "bg-indigo-600 text-white hover:bg-indigo-700",
    secondary: "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50",
    danger: "bg-red-500 text-white hover:bg-red-600",
  };

  return (
    <Component {...props} className={`${baseClasses} ${variants[variant]} ${props.className || ''}`}>
      {children}
    </Component>
  );
};
