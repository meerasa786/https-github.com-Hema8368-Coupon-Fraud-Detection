import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CheckoutPage from './pages/CheckoutPage';
import { getToken } from './api/client';

export default function App() {
  const isAuthed = !!getToken();

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/checkout" replace />} />

      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route
        path="/checkout"
        element={isAuthed ? <CheckoutPage /> : <Navigate to="/login" replace />}
      />

      <Route path="*" element={<Navigate to="/checkout" replace />} />
    </Routes>
  );
}