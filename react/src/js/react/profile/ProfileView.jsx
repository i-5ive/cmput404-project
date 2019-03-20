import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import PropTypes from "prop-types";

import ProfileHeaderView from "./ProfileHeaderView";
import ProfileStreamView from "./ProfileStreamView";
import { isExternalAuthor, getAuthorId } from "../util/AuthorUtil";
import ProfileStore from "./ProfileStore";
import LoadingComponent from "../misc/LoadingComponent";
import ProfileActions from "./ProfileActions";

const getId = (id) => {
    if (id.includes("%2Fauthor%2F")) {
        id = decodeURIComponent(id);
        if (!isExternalAuthor(id)) {
            id = getAuthorId(id);
        }
    }
    return id;
};

/**
 * Renders the view of a user's profile
 */
class ProfileView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = ProfileStore;
    }

    shouldComponentUpdate(nextProps, nextState) {
        return nextProps.match.params.id !== this.props.match.params.id ||
            this.state.isLoadingProfile !== nextState.isLoadingProfile;
    }

    _loadDetails() {
        const id = getId(this.props.match.params.id);
        ProfileActions.loadProfileDetails(id);
    }

    componentDidMount() {
        this._loadDetails();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.match.params.id !== this.props.match.params.id) {
            this._loadDetails();
        }
    }

    render() {
        if (this.state.errorLoadingProfile) {
            return (
                <Alert bsStyle="danger">
                    An error occurred while loading the user profile details.
                </Alert>
            );
        } else if (this.state.isLoadingProfile || !this.state.profileDetails) {
            return (
                <div className="center-loader">
                    <LoadingComponent />
                </div>
            );
        }
        const id = getId(this.props.match.params.id);

        return (
            <div className="profile-page">
                <div className="authorProfile">
                    <ProfileHeaderView id={id} />
                </div>
                <ProfileStreamView id={id} />
            </div>
        );
    }
}

ProfileView.propTypes = {
    match: PropTypes.object
};

export default ProfileView;
