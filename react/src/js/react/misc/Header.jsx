import React from "react";

import { Navbar, Nav, NavItem } from "react-bootstrap";

import HeaderProfileDetails from "./HeaderProfileDetails";
import Link from "react-router-dom/Link";

export default class Header extends React.Component {
    render() {
        return (
            <Navbar inverse>
                <Navbar.Header>
                    <Navbar.Brand>
                        <Link to="/">
                            Core
                        </Link>
                    </Navbar.Brand>
                </Navbar.Header>
                <Nav>
                    <NavItem componentClass={Link} href="/discover" to="/discover">
						Discover Local
                    </NavItem>
                </Nav>
                <Nav>
                    <NavItem componentClass={Link} href="/travel" to="/travel">
						Remote Travel
                    </NavItem>
                </Nav>
                <HeaderProfileDetails />
            </Navbar>
        );
    }
}
