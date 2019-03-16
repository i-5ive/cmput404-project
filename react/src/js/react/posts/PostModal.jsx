import React from "react";
import PropTypes from "prop-types";
import { Modal, ModalHeader, ModalBody, ModalTitle } from "react-bootstrap";
import CreatePost from "./CreatePost";

import { PostsActions } from "../discover/PostsStore";

export default class PostModal extends React.Component {
    static propTypes = {
        show: PropTypes.bool,
        handleClose: PropTypes.func
    }

    componentDidUpdate(prevProps) {
        if (prevProps.show !== this.props.show && this.props.show) {
            PostsActions.clearModalMessage();
        }
    }

    render() {
        return (
            <Modal
                size="lg"
                show={this.props.show}
                onHide={this.props.handleClose}
                className="create-post-modal">
                <ModalHeader closeButton>
                    <ModalTitle>
						Create Post
                    </ModalTitle>
                </ModalHeader>
                <ModalBody>
                    <CreatePost handleClose={this.props.handleClose} />
                </ModalBody>
            </Modal>
        );
    }
}
