import React, { useState } from 'react';

function AddListingPopup({ onClose, onSubmit }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [condition, setCondition] = useState('');
  const [date, setDate] = useState('');
  const [image, setImage] = useState(null);

  const handleNameChange = (event) => setName(event.target.value);
  const handlePriceChange = (event) => setPrice(event.target.value);
  const handleDescriptionChange = (event) => setDescription(event.target.value);
  const handleConditionChange = (event) => setCondition(event.target.value);
  const handleDateChange = (event) => setDate(event.target.value);
  const handleImageChange = (event) => setImage(event.target.files[0]);

  const handleSubmit = (event) => {
    event.preventDefault();

    // Call the onSubmit prop with the form data
    onSubmit({ name, price, description, condition, date, image });
  };

  return (
    <div className="add-listing-popup">
      <h2>Add Listing</h2>
      <form action="/add-item" method="POST" encType="multipart/form-data">
        <div className="form-field">
          <label>Item Name:</label>
          <input name="Item_Name" type="text" value={name} onChange={handleNameChange} />
        </div>
        <div className="form-field">
          <label>Price:</label>
          <input name="Item_Price" type="number" value={price} onChange={handlePriceChange} />
        </div>
        <div className="form-field">
          <label>Description:</label>
          <textarea name="Item_Desc" value={description} onChange={handleDescriptionChange} />
        </div>
        <div className="form-field">
          <label>Condition:</label>
          <select name="condition" value={condition} onChange={handleConditionChange}>
            <option name="condition" value="" disabled hidden>--- Select From Below ---</option>
            <option  value="Brand New" name="condition">Brand New</option>
            <option value="Like New" name="condition">Like New</option>
            <option value="Very Good " name="condition">Very Good</option>
            <option value="Good" name="condition">Good</option>
            <option value="Fair" name="condition">Fair</option>
            <option value="Poor" name="condition">Poor</option>
          </select>
        </div>
        <div className="form-field">
          <label>Auction End Date:</label>
          <input type="date" onChange={handleDateChange} />
        </div>
        <div className="form-field">
          <label>Image:</label>
          <input name="image" type="file" onChange={handleImageChange}/>
        </div>
        <button type="submit">Add Listing</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
}

export default AddListingPopup;
