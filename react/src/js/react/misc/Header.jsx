import React from "react";

import { Navbar, Nav, NavItem } from "react-bootstrap";

import HeaderProfileDetails from "./HeaderProfileDetails";

export default class Header extends React.Component {
    render() {
        return (
            <Navbar inverse>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#home">Core</a>
                    </Navbar.Brand>
                </Navbar.Header>
                <Nav>
                    <NavItem eventKey={1}>
                        Home
                    </NavItem>
                    <NavItem eventKey={2}>
                        Discover
                    </NavItem>
                </Nav>
                <HeaderProfileDetails />
            </Navbar>
        );
    }
}
