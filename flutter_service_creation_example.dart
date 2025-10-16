import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class ServiceCreationExample extends StatefulWidget {
  @override
  _ServiceCreationExampleState createState() => _ServiceCreationExampleState();
}

class _ServiceCreationExampleState extends State<ServiceCreationExample> {
  final _formKey = GlobalKey<FormState>();
  final _titleArController = TextEditingController();
  final _titleEnController = TextEditingController();
  final _descriptionArController = TextEditingController();
  final _descriptionEnController = TextEditingController();
  final _orderController = TextEditingController(text: '0');
  
  File? _selectedImage;
  bool _isActive = true;
  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;

  // Replace with your actual API base URL
  static const String BASE_URL = 'http://your-api-domain.com/api';
  static const String CREATE_SERVICE_ENDPOINT = '$BASE_URL/dashboard/services/create/';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Create Service'),
        backgroundColor: Colors.blue,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Image Selection Section
              Container(
                height: 200,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: _selectedImage == null
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.image, size: 50, color: Colors.grey),
                            SizedBox(height: 8),
                            Text('No image selected'),
                            SizedBox(height: 8),
                            ElevatedButton.icon(
                              onPressed: _pickImage,
                              icon: Icon(Icons.add_photo_alternate),
                              label: Text('Select Image'),
                            ),
                          ],
                        ),
                      )
                    : Stack(
                        children: [
                          Container(
                            width: double.infinity,
                            height: double.infinity,
                            child: Image.file(
                              _selectedImage!,
                              fit: BoxFit.cover,
                            ),
                          ),
                          Positioned(
                            top: 8,
                            right: 8,
                            child: FloatingActionButton.small(
                              onPressed: _removeImage,
                              backgroundColor: Colors.red,
                              child: Icon(Icons.close, color: Colors.white),
                            ),
                          ),
                        ],
                      ),
              ),
              SizedBox(height: 16),

              // Title Arabic Field
              TextFormField(
                controller: _titleArController,
                decoration: InputDecoration(
                  labelText: 'Title (Arabic) *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.title),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Arabic title is required';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),

              // Title English Field
              TextFormField(
                controller: _titleEnController,
                decoration: InputDecoration(
                  labelText: 'Title (English) *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.title),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'English title is required';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),

              // Description Arabic Field
              TextFormField(
                controller: _descriptionArController,
                decoration: InputDecoration(
                  labelText: 'Description (Arabic) *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.description),
                ),
                maxLines: 3,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Arabic description is required';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),

              // Description English Field
              TextFormField(
                controller: _descriptionEnController,
                decoration: InputDecoration(
                  labelText: 'Description (English) *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.description),
                ),
                maxLines: 3,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'English description is required';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),

              // Order Field
              TextFormField(
                controller: _orderController,
                decoration: InputDecoration(
                  labelText: 'Order (Display Order)',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.sort),
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Order is required';
                  }
                  if (int.tryParse(value) == null) {
                    return 'Order must be a number';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),

              // Active Status Toggle
              SwitchListTile(
                title: Text('Active Status'),
                subtitle: Text('Service will be visible to users'),
                value: _isActive,
                onChanged: (value) {
                  setState(() {
                    _isActive = value;
                  });
                },
                secondary: Icon(Icons.visibility),
              ),
              SizedBox(height: 24),

              // Error/Success Messages
              if (_errorMessage != null)
                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    border: Border.all(color: Colors.red),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error, color: Colors.red),
                      SizedBox(width: 8),
                      Expanded(child: Text(_errorMessage!, style: TextStyle(color: Colors.red))),
                    ],
                  ),
                ),
              
              if (_successMessage != null)
                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.green.shade50,
                    border: Border.all(color: Colors.green),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.check_circle, color: Colors.green),
                      SizedBox(width: 8),
                      Expanded(child: Text(_successMessage!, style: TextStyle(color: Colors.green))),
                    ],
                  ),
                ),
              
              SizedBox(height: 16),

              // Submit Button
              ElevatedButton(
                onPressed: _isLoading ? null : _createService,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  padding: EdgeInsets.symmetric(vertical: 16),
                ),
                child: _isLoading
                    ? Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                            ),
                          ),
                          SizedBox(width: 12),
                          Text('Creating Service...'),
                        ],
                      )
                    : Text('Create Service', style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _pickImage() async {
    try {
      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );
      
      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
          _errorMessage = null;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Error picking image: $e';
      });
    }
  }

  void _removeImage() {
    setState(() {
      _selectedImage = null;
    });
  }

  Future<void> _createService() async {
    // Clear previous messages
    setState(() {
      _errorMessage = null;
      _successMessage = null;
    });

    // Validate form
    if (!_formKey.currentState!.validate()) {
      return;
    }

    // Check if image is selected
    if (_selectedImage == null) {
      setState(() {
        _errorMessage = 'Please select an image for the service';
      });
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // Create multipart request
      var request = http.MultipartRequest('POST', Uri.parse(CREATE_SERVICE_ENDPOINT));
      
      // Add form fields
      request.fields['title_ar'] = _titleArController.text;
      request.fields['title_en'] = _titleEnController.text;
      request.fields['description_ar'] = _descriptionArController.text;
      request.fields['description_en'] = _descriptionEnController.text;
      request.fields['is_active'] = _isActive.toString();
      request.fields['order'] = _orderController.text;

      // Add image file
      var imageFile = await http.MultipartFile.fromPath(
        'image',
        _selectedImage!.path,
        filename: 'service_image_${DateTime.now().millisecondsSinceEpoch}.jpg',
      );
      request.files.add(imageFile);

      // Add headers
      request.headers.addAll({
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json',
      });

      // Send request
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      print('Response Status: ${response.statusCode}');
      print('Response Body: ${response.body}');

      if (response.statusCode == 201) {
        final responseData = json.decode(response.body);
        setState(() {
          _successMessage = responseData['message'] ?? 'Service created successfully!';
          _clearForm();
        });
      } else {
        final responseData = json.decode(response.body);
        setState(() {
          _errorMessage = responseData['message'] ?? 'Failed to create service';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Network error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _clearForm() {
    _titleArController.clear();
    _titleEnController.clear();
    _descriptionArController.clear();
    _descriptionEnController.clear();
    _orderController.text = '0';
    _selectedImage = null;
    _isActive = true;
  }

  @override
  void dispose() {
    _titleArController.dispose();
    _titleEnController.dispose();
    _descriptionArController.dispose();
    _descriptionEnController.dispose();
    _orderController.dispose();
    super.dispose();
  }
}

// Example usage in main.dart
void main() {
  runApp(MaterialApp(
    title: 'Service Creation Example',
    home: ServiceCreationExample(),
    theme: ThemeData(
      primarySwatch: Colors.blue,
      visualDensity: VisualDensity.adaptivePlatformDensity,
    ),
  ));
}
