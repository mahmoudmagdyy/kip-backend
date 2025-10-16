import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class UserSubServiceCreationExample extends StatefulWidget {
  @override
  _UserSubServiceCreationExampleState createState() => _UserSubServiceCreationExampleState();
}

class _UserSubServiceCreationExampleState extends State<UserSubServiceCreationExample> {
  final _formKey = GlobalKey<FormState>();
  final _titleArController = TextEditingController();
  final _titleEnController = TextEditingController();
  final _descriptionArController = TextEditingController();
  final _descriptionEnController = TextEditingController();
  final _orderController = TextEditingController(text: '0');
  final _serviceIdController = TextEditingController();
  
  File? _selectedImage;
  bool _isActive = true;
  bool _isVib = false;
  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;
  List<Map<String, dynamic>> _services = [];
  Map<String, dynamic>? _selectedService;

  // Replace with your actual API base URL
  static const String BASE_URL = 'http://your-api-domain.com/api';
  static const String CREATE_SUBSERVICE_ENDPOINT = '$BASE_URL/user/sub-services/create/';
  static const String GET_SERVICES_ENDPOINT = '$BASE_URL/user/services/';

  @override
  void initState() {
    super.initState();
    _loadServices();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Create Sub-Service (User)'),
        backgroundColor: Colors.green,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Service Selection Section
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.blue.shade200),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Select Parent Service',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue.shade800,
                      ),
                    ),
                    SizedBox(height: 12),
                    DropdownButtonFormField<Map<String, dynamic>>(
                      value: _selectedService,
                      decoration: InputDecoration(
                        labelText: 'Service *',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.category),
                      ),
                      items: _services.map((service) {
                        return DropdownMenuItem<Map<String, dynamic>>(
                          value: service,
                          child: Text('${service['title_en']} (ID: ${service['id']})'),
                        );
                      }).toList(),
                      onChanged: (value) {
                        setState(() {
                          _selectedService = value;
                          _serviceIdController.text = value?['id'].toString() ?? '';
                        });
                      },
                      validator: (value) {
                        if (value == null) {
                          return 'Please select a service';
                        }
                        return null;
                      },
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Or enter Service ID manually:',
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                    ),
                    SizedBox(height: 8),
                    TextFormField(
                      controller: _serviceIdController,
                      decoration: InputDecoration(
                        labelText: 'Service ID',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.numbers),
                      ),
                      keyboardType: TextInputType.number,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Service ID is required';
                        }
                        if (int.tryParse(value) == null) {
                          return 'Service ID must be a number';
                        }
                        return null;
                      },
                    ),
                  ],
                ),
              ),
              SizedBox(height: 24),

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
                subtitle: Text('Sub-service will be visible to users'),
                value: _isActive,
                onChanged: (value) {
                  setState(() {
                    _isActive = value;
                  });
                },
                secondary: Icon(Icons.visibility),
              ),

              // VIB Status Toggle
              SwitchListTile(
                title: Text('VIB Status'),
                subtitle: Text('Special VIB sub-service'),
                value: _isVib,
                onChanged: (value) {
                  setState(() {
                    _isVib = value;
                  });
                },
                secondary: Icon(Icons.star),
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
                onPressed: _isLoading ? null : _createSubService,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green,
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
                          Text('Creating Sub-Service...'),
                        ],
                      )
                    : Text('Create Sub-Service', style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _loadServices() async {
    try {
      final response = await http.get(Uri.parse(GET_SERVICES_ENDPOINT));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true && data['data'] != null) {
          setState(() {
            _services = List<Map<String, dynamic>>.from(data['data']);
          });
        }
      }
    } catch (e) {
      print('Error loading services: $e');
    }
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

  Future<void> _createSubService() async {
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
        _errorMessage = 'Please select an image for the sub-service';
      });
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // Create multipart request
      var request = http.MultipartRequest('POST', Uri.parse(CREATE_SUBSERVICE_ENDPOINT));
      
      // Add form fields
      request.fields['service'] = _serviceIdController.text;
      request.fields['title_ar'] = _titleArController.text;
      request.fields['title_en'] = _titleEnController.text;
      request.fields['description_ar'] = _descriptionArController.text;
      request.fields['description_en'] = _descriptionEnController.text;
      request.fields['is_active'] = _isActive.toString();
      request.fields['is_vib'] = _isVib.toString();
      request.fields['order'] = _orderController.text;

      // Add image file
      var imageFile = await http.MultipartFile.fromPath(
        'image',
        _selectedImage!.path,
        filename: 'user_subservice_image_${DateTime.now().millisecondsSinceEpoch}.jpg',
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
          _successMessage = responseData['message'] ?? 'Sub-service created successfully!';
          _clearForm();
        });
      } else {
        final responseData = json.decode(response.body);
        setState(() {
          _errorMessage = responseData['message'] ?? 'Failed to create sub-service';
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
    _serviceIdController.clear();
    _selectedImage = null;
    _selectedService = null;
    _isActive = true;
    _isVib = false;
  }

  @override
  void dispose() {
    _titleArController.dispose();
    _titleEnController.dispose();
    _descriptionArController.dispose();
    _descriptionEnController.dispose();
    _orderController.dispose();
    _serviceIdController.dispose();
    super.dispose();
  }
}

// Example usage in main.dart
void main() {
  runApp(MaterialApp(
    title: 'User Sub-Service Creation Example',
    home: UserSubServiceCreationExample(),
    theme: ThemeData(
      primarySwatch: Colors.green,
      visualDensity: VisualDensity.adaptivePlatformDensity,
    ),
  ));
}
