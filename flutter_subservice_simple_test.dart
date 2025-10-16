import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

/// Simple test example for creating a sub-service with image upload
class SimpleSubServiceTest extends StatefulWidget {
  @override
  _SimpleSubServiceTestState createState() => _SimpleSubServiceTestState();
}

class _SimpleSubServiceTestState extends State<SimpleSubServiceTest> {
  File? _selectedImage;
  bool _isLoading = false;
  String _result = '';
  final _serviceIdController = TextEditingController(text: '1'); // Default service ID

  // Replace with your actual API URL
  static const String API_URL = 'http://your-api-domain.com/api/dashboard/sub-services/create/';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Sub-Service Creation Test')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            // Service ID Input
            TextFormField(
              controller: _serviceIdController,
              decoration: InputDecoration(
                labelText: 'Service ID (Parent Service)',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.category),
              ),
              keyboardType: TextInputType.number,
            ),
            SizedBox(height: 16),

            // Image Preview
            Container(
              height: 200,
              width: double.infinity,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(8),
              ),
              child: _selectedImage == null
                  ? Center(child: Text('No image selected'))
                  : Image.file(_selectedImage!, fit: BoxFit.cover),
            ),
            SizedBox(height: 16),

            // Select Image Button
            ElevatedButton(
              onPressed: _pickImage,
              child: Text('Select Image'),
            ),
            SizedBox(height: 16),

            // Create Sub-Service Button
            ElevatedButton(
              onPressed: _isLoading ? null : _createSubService,
              child: _isLoading 
                  ? CircularProgressIndicator() 
                  : Text('Create Sub-Service'),
            ),
            SizedBox(height: 16),

            // Result Display
            if (_result.isNotEmpty)
              Expanded(
                child: Container(
                  width: double.infinity,
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: SingleChildScrollView(
                    child: Text(
                      _result,
                      style: TextStyle(fontFamily: 'monospace'),
                    ),
                  ),
                ),
              ),
          ],
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
        });
      }
    } catch (e) {
      setState(() {
        _result = 'Error picking image: $e';
      });
    }
  }

  Future<void> _createSubService() async {
    if (_selectedImage == null) {
      setState(() {
        _result = 'Please select an image first';
      });
      return;
    }

    if (_serviceIdController.text.isEmpty) {
      setState(() {
        _result = 'Please enter a service ID';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _result = 'Creating sub-service...';
    });

    try {
      // Create multipart request
      var request = http.MultipartRequest('POST', Uri.parse(API_URL));
      
      // Add required form fields
      request.fields['service'] = _serviceIdController.text;
      request.fields['title_ar'] = 'خدمة فرعية للتصميم';
      request.fields['title_en'] = 'Design Sub-Service';
      request.fields['description_ar'] = 'وصف الخدمة الفرعية بالعربية';
      request.fields['description_en'] = 'Sub-service description in English';
      request.fields['is_active'] = 'true';
      request.fields['is_vib'] = 'false';
      request.fields['order'] = '0';

      // Add image file
      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          _selectedImage!.path,
          filename: 'subservice_image.jpg',
        ),
      );

      // Send request
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      setState(() {
        _result = '''
Status Code: ${response.statusCode}
Response Body:
${response.body}
        ''';
      });

    } catch (e) {
      setState(() {
        _result = 'Error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }
}

void main() {
  runApp(MaterialApp(
    home: SimpleSubServiceTest(),
  ));
}
