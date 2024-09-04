import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { LoginApi } from "../../services/api/AuthApi.s";
import { useAuth } from "../../services/auth/AuthProvider";
import { AUTH_TOKEN_KEY } from "../../constants";

const LoginView: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, setIsAuthenticated } = useAuth();

  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  useEffect(() => {
    // set isAuthenticated to false
    if (isAuthenticated) {
      console.log("User is already authenticated. Redirecitng to User page...");
      navigate("/user");
    }
  }, []);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    if (email) {
      // Prevent page getting refreshed
      event.preventDefault();
      LoginApi(email, password)
        .then((res) => {
          // Handle successful login
          localStorage.setItem(AUTH_TOKEN_KEY, res.data.jwt);
          console.log("user loged in successfully", res);
          setIsAuthenticated(true);
          navigate("/user");
        })
        .catch((err) => {
          setIsAuthenticated(false);
          console.log("Error login user", err);
        });
    }
  };

  return (
    <>
      <div>
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              Email:
              <input
                type="text"
                onChange={(e) => setEmail(e.target.value)}
                value={email}
              />
            </label>
          </div>
          <div>
            <label>
              Password:
              <input
                type="password"
                onChange={(e) => setPassword(e.target.value)}
                value={password}
              />
            </label>
          </div>
          <div>
            <input type="submit" />
          </div>
        </form>
      </div>
    </>
  );
};
export default LoginView;
