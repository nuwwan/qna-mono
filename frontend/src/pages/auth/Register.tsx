import { useState } from "react";
import { UserRegister } from "../../services/api/AuthApi.s";

const RegisterView: React.FC = () => {
  const [firstname, setFirstname] = useState<string>("");
  const [lastname, setLastname] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    if (!!email && password == confirmPassword && firstname) {
      event.preventDefault();
      UserRegister({ email, firstname, lastname, password })
        .then((success) => {
          console.log(success);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  return (
    <>
      <div>
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              First Name:
              <input
                type="text"
                onChange={(e) => setFirstname(e.target.value)}
                value={firstname}
              />
            </label>
          </div>
          <div>
            <label>
              Last Name:
              <input
                type="text"
                onChange={(e) => setLastname(e.target.value)}
                value={lastname}
              />
            </label>
          </div>
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
            <label>
              Confirm Password:
              <input
                type="password"
                onChange={(e) => setConfirmPassword(e.target.value)}
                value={confirmPassword}
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
export default RegisterView;
