import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";

import PrivacyDropdown from "react/posts/PrivacyDropdown";

describe("PrivacyDropdown Tests", () => {
    it("should render", () => {
        const wrapper = shallow(<PrivacyDropdown />);
        expect(wrapper.find("#dropdown-privacy-button")).to.have.lengthOf(1);
    });
});
