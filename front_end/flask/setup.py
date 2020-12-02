from setuptools import find_packages from setuptools import setup  

REQUIRED_PACKAGES = [    'Flask==1.1.1', 
                        'Flask-Cors==3.0.8', 
                        'gunicorn==20.0.4']  
                        setup( 
                            name='FlaskAPI', 
                            version='1.0', 
                            install_requires=REQUIRED_PACKAGES, 
                            packages=find_packages(), 
                            include_package_data=True, 
                            description='flask api' ) 
