import React, { useState } from 'react';

function AddListingPopup({ onClose, onSubmit }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [condition, setCondition] = useState('');
  const [image, setImage] = useState(null);

  const handleNameChange = (event) => setName(event.target.value);
  const handlePriceChange = (event) => setPrice(event.target.value);
  const handleDescriptionChange = (event) => setDescription(event.target.value);
  const handleConditionChange = (event) => setCondition(event.target.value);
  const handleImageChange = (event) => setImage(event.target.files[0]);

  const handleSubmit = (event) => {
    event.preventDefault();

    // Call the onSubmit prop with the form data
    onSubmit({ name, price, description, condition, image });
  };

  return (
    <div className="add-listing-popup">
      <h2>Add Listing</h2>
      <form onSubmit={handleSubmit}>
        <div class="form-field">
          <label>Name:</label>
          <input type="text" value={name} onChange={handleNameChange} />
        </div>
        <div class="form-field">
          <label>Price:</label>
          <input type="text" value={price} onChange={handlePriceChange} />
        </div>
        <div class="form-field">
          <label>Description:</label>
          <textarea value={description} onChange={handleDescriptionChange} />
        </div>
        <div class="form-field">
          <label>Condition:</label>
          <select value={condition} onChange={handleConditionChange}>
            <option value="Brand New">Brand New</option>
            <option value="Like New">Like New</option>
            <option value="Very Good">Very Good</option>
            <option value="Good">Good</option>
            <option value="Fair">Fair</option>
            <option value="Poor">Poor</option>
          </select>
        </div>
        <div class="form-field">
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
