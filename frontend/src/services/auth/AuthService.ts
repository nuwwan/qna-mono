import { AUTH_TOKEN_KEY } from "../../constants";
import { redirect } from "react-router-dom";

export const logoutUser = () => {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  return redirect("/login");
};
