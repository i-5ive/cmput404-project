import React from "react";
import PropTypes from "prop-types";
import { DropdownButton, MenuItem } from "react-bootstrap";

import privacyConfig from "./constants/PrivacyDropdownConfig";

export default class PrivacyDropdown extends React.Component {
    static propTypes = {
        handleSelect: PropTypes.func.isRequired
    }

    constructor(props) {
        super(props);

        this.state = {
            title: "Public"
        };
    }

    onItemSelect = (title, key) => {
        this.setState({ title }, () => {
            this.props.handleSelect(key);
        });
    }

    // Can probably change this
    onCustomClick = (key) => {
        if (key === "custom") {
            this.renderCustomAuthorModal();
        }
    }

    // TODO How are we going to handle "custom authors"
    // Facebook TM has a modal that pops up
    renderCustomAuthorModal = () => {
    }

    render() {
        return (
            <DropdownButton id="dropdown-privacy-button" title={this.state.title}>
                {privacyConfig.map((item) =>
                    <MenuItem key={item.key}
                        eventKey={item.key}
                        onSelect={() => this.onItemSelect(item.title, item.key)}
                        onClick={() => this.onCustomClick(item.key)}>
                        {item.title}
                    </MenuItem>
                )}
            </DropdownButton>
        );
    }
}
