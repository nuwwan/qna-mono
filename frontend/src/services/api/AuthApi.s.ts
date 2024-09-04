import { TRegisterUser } from "../../types/Auth.t";
import { api } from "./BaseApi.s";

const LOGIN_URL = "/auth/login";
const USER_DETAILS_URL = "/auth/user";
const USER_REGISTER_URL = "/auth/register";
const LOGOUT_URL = "/auth/logout";

export const LoginApi = (email: string, password: string) => {
  return api.post(LOGIN_URL, { email: email, password: password });
};

export const UserDetailsAPI = () => {
  return api.get(USER_DETAILS_URL);
};

export const UserLogout = () => {
  return api.get(LOGOUT_URL);
};

export const UserRegister = (data: TRegisterUser) => {
  return api.post(USER_REGISTER_URL, data);
};
