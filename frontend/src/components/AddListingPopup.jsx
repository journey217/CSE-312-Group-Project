import React, { useState } from 'react';

function AddListingPopup({ onClose, onSubmit }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [condition, setCondition] = useState('');
  const [category, setCategory] = useState('');
  const [image, setImage] = useState(null);

  const handleNameChange = (event) => setName(event.target.value);
  const handlePriceChange = (event) => setPrice(event.target.value);
  const handleDescriptionChange = (event) => setDescription(event.target.value);
  const handleConditionChange = (event) => setCondition(event.target.value);
  const handleCategoryChange = (event) => setCategory(event.target.value);
  const handleImageChange = (event) => setImage(event.target.files[0]);

  const handleSubmit = (event) => {
    event.preventDefault();

    // Call the onSubmit prop with the form data
    onSubmit({ name, price, description, condition, category, image });
  };

  return (
    <div className="add-listing-popup">
      <h2>Add Listing</h2>
      <form action="/add-item" method="post">
        <div className="form-field">
          <label>Item Name:</label>
          <input type="text" value={name} onChange={handleNameChange} />
        </div>
        <div className="form-field">
          <label>Base Price:</label>
          <input name="Item_Price" type="number" value={price} onChange={handlePriceChange} />
        </div>
        <div class="form-field">
          <label>Description:</label>
          <textarea value={description} onChange={handleDescriptionChange} />
        </div>
        <div class="form-field">
          <label>Condition:</label>
          <select value={condition} onChange={handleConditionChange}>
            <option value="" disabled hidden>--- Select From Below ---</option>            <option value="Brand New">Brand New</option>
            <option value="Like New">Like New</option>
            <option value="Very Good">Very Good</option>
            <option value="Good">Good</option>
            <option value="Fair">Fair</option>
            <option value="Poor">Poor</option>
          </select>
        </div>
        <div className="form-field">
          <label>Auction End Date:</label>
          <input type="date" onChange={handleDateChange} />
        </div>
        <div className="form-field">
          <label>Image:</label>
          <input type="file" onChange={handleImageChange} />
        </div>
        <button type="submit">Add Listing</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
}

export default AddListingPopup;
