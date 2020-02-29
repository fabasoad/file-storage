import React from 'react';
import { shallow } from 'enzyme';
import UploadFile from '../../components/UploadFile';

let wrapper, handleUploadFile;

beforeEach(() => {
    handleUploadFile = jest.fn();
    wrapper = shallow(<UploadFile handleUploadFile={handleUploadFile} />);
});

test('should render UploadFile correctly', () => {
    expect(wrapper).toMatchSnapshot();
});

test('should handle handleUploadFile', () => {
    const expectedFileName = 'file1.txt';
    wrapper.find('form').prop('onSubmit')({
        preventDefault: () => {},
        target: { elements: { file: { value: expectedFileName } } }
    });
    expect(handleUploadFile).toHaveBeenLastCalledWith(expectedFileName);
});