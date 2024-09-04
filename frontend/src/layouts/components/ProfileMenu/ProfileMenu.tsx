import { Dropdown, Menu, Modal } from "antd";
import React, { useState } from "react";

import {
  SettingOutlined,
  LoginOutlined,
  UserOutlined,
} from "@ant-design/icons";

import "./ProfileMenu.scss";
import { logoutUser } from "../../../services/auth/AuthService";

const ProfileMenu: React.FC = () => {
  const [isLogoutPopupOpen, setIsLogoutPopupOpen] = useState<boolean>(false);

  const handleLogOut = (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    setIsLogoutPopupOpen(true);
  };

  const handleLogoutOk = () => {
    logoutUser();
    setIsLogoutPopupOpen(false);
  };

  const handleLogOutCancel = () => {
    setIsLogoutPopupOpen(false);
  };

  const menuItems = (
    <Menu style={{ width: 150 }}>
      <Menu.Item key="1">
        <a href="/profile">
          <UserOutlined /> Profile
        </a>
      </Menu.Item>
      <Menu.Item key="2">
        <a href="/settings">
          <SettingOutlined /> Settings
        </a>
      </Menu.Item>
      <Menu.Item key="3">
        <a href="/logout" onClick={handleLogOut}>
          <LoginOutlined /> Logout
        </a>
      </Menu.Item>
    </Menu>
  );

  return (
    <div style={{ display: "flex", marginLeft: "auto" }}>
      <Dropdown overlay={menuItems} placement="bottom" className="profile-menu">
        <a
          className="ant-dropdown-link"
          onClick={(e) => e.preventDefault()}
          style={{ marginLeft: 20, marginRight: 20 }}
        >
          <UserOutlined />
        </a>
      </Dropdown>
      <Modal
        title="Confirm Logout"
        open={isLogoutPopupOpen}
        onOk={handleLogoutOk}
        onCancel={handleLogOutCancel}
      >
        <p>Are you sure you want to logout?</p>
      </Modal>
    </div>
  );
};

export default ProfileMenu;
