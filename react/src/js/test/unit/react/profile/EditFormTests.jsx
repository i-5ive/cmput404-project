import React from "react";
import Reflux from "reflux";
import { expect } from "chai";
import { shallow } from "enzyme";

import ProfileDetailsForm from "react/profile/ProfileDetailsForm";
import ProfileStore from "react/profile/ProfileStore";

const defaultEditProfileDetails = {
    displayName: "hello",
    firstName: "",
    lastName: "",
    email: "",
    github: "",
    bio: ""
};

 describe("Tests the ProfileDetailsForm component validation", () => {
    let wrapper = null;

    beforeEach(() => {
        const store = Reflux.initStore(ProfileStore);
        store.setState({
			editProfileDetails: defaultEditProfileDetails
        });
        wrapper = shallow(<ProfileDetailsForm />);
    });

    it("tests _validateDisplayName with an empty name", () => {
        expect(wrapper.instance()._validateDisplayName("")).to.be.ok;
    });

    it("tests _validateDisplayName with a long name", () => {
        expect(wrapper.instance()._validateDisplayName("a".repeat(81))).to.be.ok;
    });

    it("tests _validateDisplayName with a name that has allowed characters but no alphanumeric ones", () => {
        expect(wrapper.instance()._validateDisplayName("_-")).to.be.ok;
    });

    it("tests _validateDisplayName with a name that has only alphanumeric characters", () => {
        expect(wrapper.instance()._validateDisplayName("abcdefFgLK209")).to.be.not.ok;
    });

    it("tests _validateDisplayName with a name that has alphanumeric and allowed special characters", () => {
        expect(wrapper.instance()._validateDisplayName("abcdefFgLK209 aaa-_aaa")).to.be.not.ok;
    });

    it("tests _validateName with an empty name", () => {
        expect(wrapper.instance()._validateName("")).to.be.not.ok;
    });

    it("tests _validateName with a long name", () => {
        expect(wrapper.instance()._validateName("a".repeat(50))).to.be.ok;
    });

    it("tests _validateName with a name that has allowed characters but no alphanumeric ones", () => {
        expect(wrapper.instance()._validateName("_-")).to.be.ok;
    });

    it("tests _validateName with a name that has only alphanumeric characters", () => {
        expect(wrapper.instance()._validateName("abcdefFgLK209")).to.be.not.ok;
    });

    it("tests _validateName with a name that has alphanumeric and allowed special characters", () => {
        expect(wrapper.instance()._validateName("abcdefFgLK209 aaa-_aaa")).to.be.not.ok;
    });

    it("tests _validateEmail with an empty email", () => {
        expect(wrapper.instance()._validateEmail("")).to.be.not.ok;
    });

    it("tests _validateEmail with an invalid email missing domain", () => {
        expect(wrapper.instance()._validateEmail("x@.com")).to.be.ok;
    });

    it("tests _validateEmail with an invalid email missing @", () => {
        expect(wrapper.instance()._validateEmail("xy.com")).to.be.ok;
    });

    it("tests _validateEmail with a valid email", () => {
        expect(wrapper.instance()._validateEmail("test@ualberta.ca")).to.be.not.ok;
    });

    it("tests _validateEmail with a long email", () => {
        expect(wrapper.instance()._validateEmail("test".repeat(40) + "@ualberta.ca")).to.be.ok;
    });

    it("tests _validateGithub with an invalid github url", () => {
        expect(wrapper.instance()._validateGithub("https://notgithub.com/not_a_user")).to.be.ok;
    });

    it("tests _validateGithub with a valid github url", () => {
        expect(wrapper.instance()._validateGithub("https://github.com/not_a_user")).to.be.not.ok;
    });

    it("tests _validateGithub with a valid github url with www.", () => {
        expect(wrapper.instance()._validateGithub("https://www.github.com/not_a_user")).to.be.not.ok;
    });

    it("tests _validateGithub with an invalid github url path", () => {
        expect(wrapper.instance()._validateGithub("https://github.com/not_a_user/invalid")).to.be.ok;
    });

    it("tests _validateGithub with an empty github url", () => {
        expect(wrapper.instance()._validateGithub("")).to.be.not.ok;
    });

    it("tests _validateBio with an empty bio", () => {
        expect(wrapper.instance()._validateBio("")).to.be.not.ok;
    });

    it("tests _validateBio with a short bio", () => {
        expect(wrapper.instance()._validateBio("This is a short bio")).to.be.not.ok;
    });

    it("tests _validateBio with a long bio", () => {
        expect(wrapper.instance()._validateBio("This is a long bio".repeat(100))).to.be.ok;
    });
});