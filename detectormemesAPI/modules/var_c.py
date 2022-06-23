#MongoDB strings
MONGO_DATABASE_NAME = 'imagenes'
MONGO_IP = "mongodb://localhost:27017/"

# Images database collection
MONGO_IMAGE_COLLECTION = 'imagenes_pruebas'

# U_CREDITS database collection
MONGO_U_CREDITS_COLLECTION = 'u_credits'

# Payments database collection
MONGO_U_PAY_COLLECTION = 'u_pay'

# Permissions database collection
MONGO_U_PERMISSIONS_COLLECTION = 'u_permissions'

# Garbage characters regExp
reg_exp_garbage_characters = r"([A-Z])\w+|([0-9])\w+/gi"

# Source regExp
reg_exp_instagram = r"/(Instagram)?(instagram)?/g"
reg_exp_reddit = r"/(Reddit)?(reddit)?/g"
reg_exp_twitter = r"/(Twitter)?(twitter)?/g"