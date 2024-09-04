import { Menu } from "antd";
import AppIcon from "./AppIcon";
import ProfileMenu from "./ProfileMenu/ProfileMenu";

const MainHeader: React.FC = () => {
  return (
    <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["2"]}>
      <div>
        <AppIcon />
      </div>
      <ProfileMenu />
    </Menu>
  );
};

export default MainHeader;
