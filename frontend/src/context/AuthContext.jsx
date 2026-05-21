import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext(null);

const API_BASE_URL = 'http://localhost:8000';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('tracemark_token'));
  const [isLoadingUser, setIsLoadingUser] = useState(true);

  // Token değiştiğinde localStorage'ı güncelle
  useEffect(() => {
    if (token) {
      localStorage.setItem('tracemark_token', token);
      fetchCurrentUser(token);
    } else {
      localStorage.removeItem('tracemark_token');
      setUser(null);
      setIsLoadingUser(false);
    }
  }, [token]);

  const fetchCurrentUser = async (currentToken) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${currentToken}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        // Token geçersiz ya da süresi dolmuş
        setToken(null);
      }
    } catch {
      setToken(null);
    } finally {
      setIsLoadingUser(false);
    }
  };

  const googleLogin = async (googleCredential) => {
    const res = await fetch(`${API_BASE_URL}/api/auth/google`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: googleCredential }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Google ile giriş başarısız.');

    setToken(data.access_token);
    return data;
  };

  const login = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email); // OAuth2PasswordRequestForm username bekliyor
    formData.append('password', password);

    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Giriş başarısız.');

    setToken(data.access_token);
    return data;
  };

  const register = async (fullName, email, password) => {
    const res = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ full_name: fullName, email, password }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Kayıt başarısız.');
    return data;
  };

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
  }, []);

  // Authenticated fetch helper — token'ı otomatik ekler
  const authFetch = useCallback(
    async (url, options = {}) => {
      return fetch(url, {
        ...options,
        headers: {
          ...(options.headers || {}),
          Authorization: `Bearer ${token}`,
        },
      });
    },
    [token]
  );

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, googleLogin, authFetch, isLoadingUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
}
