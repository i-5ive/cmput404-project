import React from "react";
import PropTypes from "prop-types";
import { Modal, ModalHeader, ModalBody } from "react-bootstrap";
import CreatePost from "./CreatePost";

export default class PostModal extends React.Component {
    static propTypes = {
        show: PropTypes.bool,
        handleClose: PropTypes.func
    }

    constructor(props) {
        super(props);
        this.state = {
            show: this.props.show
        };
    }

    shouldComponentUpdate(nextProps, nextState) {
        return (this.props.show !== nextProps.show);
    }

    render() {
        return (
            <Modal
                size="lg"
                show={this.props.show}
                onHide={this.props.handleClose}
                className="create-post-modal">
                <ModalHeader closeButton>Create Post</ModalHeader>
                <ModalBody>
                    <CreatePost handleClose={this.props.handleClose} />
                </ModalBody>
            </Modal>
        );
    }
}
