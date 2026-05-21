import React, { useState } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../context/AuthContext';

// Shared divider + Google button — placed at the BOTTOM of each form
function GoogleAuthButton({ onClose, setError, setIsLoading }) {
  const { googleLogin } = useAuth();

  return (
    <div className="w-full mt-4">
      <div className="flex items-center gap-3 mb-4">
        <div className="flex-1 h-px bg-gray-200" />
        <span className="text-xs text-gray-400 font-medium">veya Google ile devam et</span>
        <div className="flex-1 h-px bg-gray-200" />
      </div>
      <div className="flex justify-center">
        <GoogleLogin
          onSuccess={async (credentialResponse) => {
            setError(null);
            setIsLoading(true);
            try {
              await googleLogin(credentialResponse.credential);
              onClose();
            } catch (err) {
              setError(err.message);
            } finally {
              setIsLoading(false);
            }
          }}
          onError={() => setError('Google ile giriş başarısız oldu. Tekrar deneyin.')}
          useOneTap={false}
          theme="outline"
          size="large"
          text="continue_with"
          shape="rectangular"
          width="360"
          locale="tr"
        />
      </div>
    </div>
  );
}

// ── LOGIN MODAL ────────────────────────────────────────────────────────────────
export function LoginModal({ onClose, onSwitchToRegister }) {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login(email, password);
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />

      <div
        className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-fade-in"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="h-1.5 w-full bg-gradient-to-r from-primary to-secondary" />

        <div className="p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Giriş Yap</h2>
              <p className="text-sm text-gray-500 mt-1">TraceMark hesabına giriş yap</p>
            </div>
            <button
              onClick={onClose}
              className="w-9 h-9 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400 hover:text-gray-600"
            >
              <i className="ri-close-line text-xl" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">E-posta</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <i className="ri-mail-line text-gray-400" />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={isLoading}
                  placeholder="ornek@email.com"
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary focus:border-primary transition-colors disabled:bg-gray-50"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Şifre</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <i className="ri-lock-line text-gray-400" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-11 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary focus:border-primary transition-colors disabled:bg-gray-50"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600"
                >
                  <i className={showPassword ? 'ri-eye-off-line' : 'ri-eye-line'} />
                </button>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm border border-red-200 flex items-start gap-2">
                <i className="ri-error-warning-line mt-0.5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 rounded-lg font-semibold text-white transition-all flex items-center justify-center gap-2 ${
                isLoading
                  ? 'bg-primary/60 cursor-not-allowed'
                  : 'bg-primary hover:bg-blue-600 shadow-lg shadow-primary/30 hover:shadow-primary/40'
              }`}
            >
              {isLoading ? (
                <>
                  <i className="ri-loader-4-line animate-spin text-lg" />
                  Giriş yapılıyor...
                </>
              ) : (
                <>
                  <i className="ri-login-box-line text-lg" />
                  Giriş Yap
                </>
              )}
            </button>
          </form>

          {/* Google button — BOTTOM */}
          <GoogleAuthButton onClose={onClose} setError={setError} setIsLoading={setIsLoading} />

          <p className="text-center text-sm text-gray-500 mt-5">
            Hesabın yok mu?{' '}
            <button onClick={onSwitchToRegister} className="text-primary font-semibold hover:underline">
              Kayıt Ol
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

// ── REGISTER MODAL ─────────────────────────────────────────────────────────────
export function RegisterModal({ onClose, onSwitchToLogin }) {
  const { register, login } = useAuth();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== passwordConfirm) {
      setError('Şifreler eşleşmiyor.');
      return;
    }
    if (password.length < 6) {
      setError('Şifre en az 6 karakter olmalıdır.');
      return;
    }

    setIsLoading(true);
    try {
      await register(fullName, email, password);
      await login(email, password);
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />

      <div
        className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-fade-in"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="h-1.5 w-full bg-gradient-to-r from-primary to-secondary" />

        <div className="p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Kayıt Ol</h2>
              <p className="text-sm text-gray-500 mt-1">Yeni bir TraceMark hesabı oluştur</p>
            </div>
            <button
              onClick={onClose}
              className="w-9 h-9 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400 hover:text-gray-600"
            >
              <i className="ri-close-line text-xl" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Full Name */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Ad Soyad</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <i className="ri-user-line text-gray-400" />
                </div>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                  disabled={isLoading}
                  placeholder="Adın Soyadın"
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary focus:border-primary transition-colors disabled:bg-gray-50"
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">E-posta</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <i className="ri-mail-line text-gray-400" />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={isLoading}
                  placeholder="ornek@email.com"
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary focus:border-primary transition-colors disabled:bg-gray-50"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Şifre</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <i className="ri-lock-line text-gray-400" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  placeholder="Minimum 6 karakter"
                  className="w-full pl-10 pr-11 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary focus:border-primary transition-colors disabled:bg-gray-50"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600"
                >
                  <i className={showPassword ? 'ri-eye-off-line' : 'ri-eye-line'} />
                </button>
              </div>
            </div>

            {/* Password Confirm */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Şifre Tekrar</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <i className="ri-lock-password-line text-gray-400" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={passwordConfirm}
                  onChange={(e) => setPasswordConfirm(e.target.value)}
                  required
                  disabled={isLoading}
                  placeholder="Şifreni tekrar gir"
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary focus:border-primary transition-colors disabled:bg-gray-50"
                />
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm border border-red-200 flex items-start gap-2">
                <i className="ri-error-warning-line mt-0.5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 rounded-lg font-semibold text-white transition-all flex items-center justify-center gap-2 mt-2 ${
                isLoading
                  ? 'bg-primary/60 cursor-not-allowed'
                  : 'bg-primary hover:bg-blue-600 shadow-lg shadow-primary/30 hover:shadow-primary/40'
              }`}
            >
              {isLoading ? (
                <>
                  <i className="ri-loader-4-line animate-spin text-lg" />
                  Hesap oluşturuluyor...
                </>
              ) : (
                <>
                  <i className="ri-user-add-line text-lg" />
                  Hesap Oluştur
                </>
              )}
            </button>
          </form>

          {/* Google button — BOTTOM */}
          <GoogleAuthButton onClose={onClose} setError={setError} setIsLoading={setIsLoading} />

          <p className="text-center text-sm text-gray-500 mt-5">
            Zaten hesabın var mı?{' '}
            <button onClick={onSwitchToLogin} className="text-primary font-semibold hover:underline">
              Giriş Yap
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
