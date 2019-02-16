import React from "react";
import { expect } from "chai";
import NewPostButton from "react/posts/NewPostButton";
import { shallow } from "enzyme";

describe("NewPostButton Tests", () => {
    it("renders via shallow", () => {
        const page = shallow(<NewPostButton />);

        //expect(page.text()).to.contain("Page Not Found!");
    });

    it('renders without crashing via dom', () => {
      const div = document.createElement('div');
      ReactDOM.render(<NewPostButton />, div);
      ReactDOM.unmountComponentAtNode(div);
    });
});
