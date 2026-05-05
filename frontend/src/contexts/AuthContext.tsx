import React, { createContext, useContext, useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  user: User | null;
}

interface User {
  id: string;
  email: string;
  name: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const isDevelopmentAuthEnabled = () => import.meta.env.DEV || import.meta.env.MODE === "test";

const createDevelopmentUser = (): User => ({
  id: "1",
  email: "dev@llb.com",
  name: "Development User",
});

const getBrowserStorage = (): Storage | null => {
  if (typeof localStorage === "undefined") return null;
  return localStorage;
};

const getInitialAuthState = (): Pick<AuthContextType, "isAuthenticated" | "user"> => {
  const storage = getBrowserStorage();
  const token = typeof storage?.getItem === "function" ? storage.getItem("auth_token") : null;

  if (token) {
    return {
      isAuthenticated: true,
      user: {
        id: "1",
        email: "user@example.com",
        name: "Test User",
      },
    };
  }

  if (isDevelopmentAuthEnabled()) {
    if (typeof storage?.setItem === "function") {
      storage.setItem("auth_token", "dev_token");
    }
    return {
      isAuthenticated: true,
      user: createDevelopmentUser(),
    };
  }

  return { isAuthenticated: false, user: null };
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const initialAuthState = React.useMemo(() => getInitialAuthState(), []);
  const [isAuthenticated, setIsAuthenticated] = useState(initialAuthState.isAuthenticated);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState<User | null>(initialAuthState.user);
  const { t } = useTranslation();

  useEffect(() => {
    // Check for existing session
    const checkAuth = async () => {
      try {
        const storage = getBrowserStorage();
        const token = typeof storage?.getItem === "function" ? storage.getItem("auth_token") : null;
        if (token) {
          // TODO: Validate token with backend
          setIsAuthenticated(true);
          // TODO: Fetch user data
          setUser({
            id: "1",
            email: "user@example.com",
            name: "Test User",
          });
        } else if (isDevelopmentAuthEnabled()) {
          // Auto-login for development only
          if (typeof storage?.setItem === "function") {
            storage.setItem("auth_token", "dev_token");
          }
          setIsAuthenticated(true);
          setUser(createDevelopmentUser());
        } else {
          setIsAuthenticated(false);
          setUser(null);
        }
      } catch (error) {
        console.error("Auth check failed:", error);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      // TODO: Implement actual login API call
      // For now, simulate successful login
      const mockToken = "mock_token";
      const storage = getBrowserStorage();
      if (typeof storage?.setItem === "function") {
        storage.setItem("auth_token", mockToken);
      }
      setIsAuthenticated(true);
      setUser({
        id: "1",
        email,
        name: "Test User",
      });
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      setIsLoading(true);
      // TODO: Implement actual logout API call
      const storage = getBrowserStorage();
      if (typeof storage?.removeItem === "function") {
        storage.removeItem("auth_token");
      }
      setIsAuthenticated(false);
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, isLoading, login, logout, user }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
