import React from "react";
import { expect } from "chai";
import NotFoundPage from "react/help/PageNotFound";
import { shallow } from "enzyme";

describe("PageNotFound Tests", () => {
    it("renders", () => {
        const page = shallow(<NotFoundPage />);

        expect(page.text()).to.contain("Page Not Found!");
    });
});
