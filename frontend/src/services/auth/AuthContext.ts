import { createContext } from "react";
import { AUTH_TOKEN_KEY } from "../../constants";

type IAuthContext = {
  isAuthenticated: boolean;
  setIsAuthenticated: (newState: boolean) => void;
};

// Default value for auth cotext
export const initialValue: IAuthContext = {
  isAuthenticated: localStorage.getItem(AUTH_TOKEN_KEY) ? true : false,
  setIsAuthenticated: () => {},
};

export const AuthContext = createContext<IAuthContext>(initialValue);
