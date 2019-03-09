import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import ProfileStore from "./ProfileStore";
import LoadingComponent from "../misc/LoadingComponent";
import ProfileActions from "./ProfileActions";

/**
 * Renders details about a user's github repositories
 */
export default class ProfileGithubDetails extends Reflux.Component {
  constructor(props) {
    super(props);
    this.store = ProfileStore;
  }

  _loadGithub() {
    ProfileActions.loadGithubDetails(this.state.profileDetails.github);
  }

  componentDidMount() {
    if (this.state.profileDetails.github && !this.state.githubDetails) {
      this._loadGithub();
    }
  }

  shouldComponentUpdate(nextProps, nextState) {
    return this.state.profileDetails.github !== nextState.profileDetails.github ||
            this.state.githubDetails !== nextState.githubDetails ||
            this.state.errorLoadingGithubRepos !== nextState.errorLoadingGithubRepos;
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.profileDetails.github && this.state.profileDetails.github !== prevState.profileDetails.github) {
      this._loadGithub();
    }
  }

  renderRepo(repo) {
    return (
      <div key={repo.url}>
        <a href={repo.url} target="_blank">
          {
            repo.name
          }
        </a>
        <br />
      </div>
    );
  }

  render() {
    if (!this.state.profileDetails.github) {
      return <h5>This user has not enabled github integration.</h5>;
    } else if (this.state.errorLoadingGithubRepos) {
      return (
        <Alert bsStyle="danger">
                    An error occurred while loading github details.
        </Alert>
      );
    } else if (!this.state.githubDetails) {
      return <LoadingComponent />;
    }
    return (
      <div className="repos">
        {
          this.state.githubDetails.map(this.renderRepo)
        }
      </div>
    );
  }
}
