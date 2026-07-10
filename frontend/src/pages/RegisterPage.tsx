import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { ErrorAlert } from '../components/ErrorAlert';
import { Card } from '../components/Card';
import { UserPlus } from 'lucide-react';

export const RegisterPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [full_name, setFullName] = useState('');
  const [error, setError] = useState('');
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register({ email, password, full_name, role: 'member' });
      navigate('/');
    } catch (err: any) {
      const responseData = err.response?.data;
      if (responseData?.detail && Array.isArray(responseData.detail)) {
        const errorMessages = responseData.detail.map((err: any) => `${err.loc[1]}: ${err.msg}`);
        setError(errorMessages);
      } else if (responseData?.detail) {
        setError(responseData.detail);
      } else {
        setError('Registration failed');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-2"><UserPlus className="text-indigo-600"/> Register</h2>
        {error && <ErrorAlert message={error} />}
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Full Name" type="text" value={full_name} onChange={(e) => setFullName(e.target.value)} required />
          <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Button type="submit" className="w-full">Create Account</Button>
        </form>
      </Card>
    </div>
  );
};
